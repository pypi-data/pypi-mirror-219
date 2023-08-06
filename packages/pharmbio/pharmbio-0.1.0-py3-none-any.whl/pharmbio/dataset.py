import os
import polars as pl
from typing import Union, List

DB_URI = "postgresql://pharmbio_readonly:readonly@imagedb-pg-postgresql.services.svc.cluster.local/imagedb"


def get_projects_list(lookup: str = None):
    query = """
        SELECT project
        FROM image_analyses_per_plate
        GROUP BY project
        ORDER BY project 
        """
    project_list = pl.read_database(query, DB_URI).to_dict(as_series=False)["project"]
    project_list = list(filter(None, project_list))
    if lookup is not None:
        lookup = lookup.lower()
        project_list = [s for s in project_list if lookup in s.lower()]
    return project_list


def get_qc_info(
    name: str,
    drop_replication: Union[str, List[int]] = "Auto",
    keep_replication: Union[str, List[int]] = "None",
    filter: dict = None,
):  # sourcery skip: low-code-quality
    # Query database and store result in Polars dataframe
    query = f"""
            SELECT *
            FROM image_analyses_per_plate
            WHERE project ILIKE '%%{name}%%'
            AND meta->>'type' = 'cp-qc'
            AND analysis_date IS NOT NULL
            ORDER BY plate_barcode 
            """
    qc_info_df = pl.read_database(query, DB_URI)
    data_dict = (
        qc_info_df.select(["project", "plate_barcode"])
        .groupby("project")
        .agg(pl.col("plate_barcode"))
        .to_dicts()
    )
    unique_project_count = qc_info_df.unique("project").height
    if unique_project_count == 0:
        message = f"Quering the db for {name} returned nothing."
    elif unique_project_count > 1:
        message = f"Quering the db for {name} found {unique_project_count} studies: {qc_info_df.unique('project')['project'].to_list()}"
    else:
        message = f"Quering the db for {name} found {unique_project_count} study: {qc_info_df.unique('project')['project'].to_list()}"
    print(f"{message}\n{'_'*50}")
    if unique_project_count != 0:
        for i, study in enumerate(data_dict, start=1):
            print(i)
            for value in study.values():
                print("\t" + str(value))
    print("_" * 50)
    grouped_replicates = qc_info_df.groupby("plate_barcode")
    for plate_name, group in grouped_replicates:
        if len(group) > 1:
            print(
                f"Analysis for the plate with barcode {plate_name} is replicated {len(group)} times with analysis_id of {sorted(group['analysis_id'].to_list())}"
            )
    if qc_info_df.filter(pl.col("plate_barcode").is_duplicated()).is_empty():
        print("No replicated analysis has been found!")
    if drop_replication == "Auto" and keep_replication == "None":
        # keeping the highest analysis_id value of replicated rows
        qc_info_df = (
            qc_info_df.sort("analysis_id", descending=True)
            .unique("plate_barcode", keep="first")
            .sort("analysis_id")
        )
    elif isinstance(drop_replication, list):
        # drop rows by analysis_id
        qc_info_df = qc_info_df.filter(~pl.col("analysis_id").is_in(drop_replication))
    elif isinstance(keep_replication, list):
        # drop rows by analysis_id
        qc_info_df = qc_info_df.filter(pl.col("analysis_id").is_in(keep_replication))

    if filter is None:
        return qc_info_df
    conditions = []
    # Iterate over each key-value pair in the filter dictionary
    for key, values in filter.items():
        # Create an OR condition for each value associated with a key
        key_conditions = [pl.col(key).str.contains(val) for val in values]
        combined_key_condition = key_conditions[0]
        for condition in key_conditions[1:]:
            combined_key_condition = combined_key_condition | condition
        conditions.append(combined_key_condition)
    # Combine all conditions with AND
    final_condition = conditions[0]
    for condition in conditions[1:]:
        final_condition = final_condition & condition
    # Apply the condition to the DataFrame
    return qc_info_df.filter(final_condition)


def _get_file_extension(filename):
    """Helper function to get file extension"""
    possible_extensions = [".parquet", ".csv", ".tsv"]
    for ext in possible_extensions:
        full_filename = filename + ext
        if os.path.isfile(full_filename):
            return ext
    print(f"Warning: File {filename} with extensions {possible_extensions} not found.")
    return None


def _read_file(filename, extension):
    """Helper function to read file based on its extension"""
    if extension == ".parquet":
        return pl.read_parquet(filename + extension)
    elif extension in [".csv", ".tsv"]:
        delimiter = "," if extension == ".csv" else "\t"
        return pl.read_csv(filename + extension, separator=delimiter)
    return None


def get_qc_data(filtered_qc_info):
    # Add qc-file column based on 'results' and 'plate_barcode' columns
    filtered_qc_info = filtered_qc_info.with_columns(
        (pl.col("results") + "qcRAW_images_" + pl.col("plate_barcode")).alias("qc-file")
    )
    print(
        f"\n{'_'*50}\nQuality control data of {filtered_qc_info.height} plates imported:\n"
    )
    # Read and process all the files in a list, skipping files not found
    dfs = []
    for row in filtered_qc_info.iter_rows(named=True):
        ext = _get_file_extension(row["qc-file"])
        print(f"\t{row['qc-file']}{ext}")
        if ext is not None:
            df = _read_file(row["qc-file"], ext)
            df = df.with_columns(
                pl.lit(row["plate_acq_id"]).alias("Metadata_AcqID"),
                pl.lit(row["plate_barcode"]).alias("Metadata_Barcode"),
            )
            dfs.append(df)
    # Concatenate all the dataframes at once and return it
    return pl.concat(dfs, how="vertical")


class ExperimentData:
    def __init__(
        self,
        name: str,
        drop_replication: Union[str, List[int]] = "Auto",
        keep_replication: Union[str, List[int]] = "None",
        filter: dict = None,
    ) -> None:
        self.qc_info = get_qc_info(name, drop_replication, keep_replication, filter)
        self.qc_data = get_qc_data(self.qc_info)
        self.project = sorted(self.qc_info["project"].unique().to_list())
        self.pipeline_name = sorted(self.qc_info["pipeline_name"].unique().to_list())
        self.analysis_date = sorted(self.qc_info["analysis_date"].unique().to_list())
        self.plate_barcode = sorted(self.qc_info["plate_barcode"].unique().to_list())
        self.plate_acq_name = sorted(self.qc_info["plate_acq_name"].unique().to_list())
        self.plate_acq_id = sorted(self.qc_info["plate_acq_id"].unique().to_list())
        self.analysis_id = sorted(self.qc_info["analysis_id"].unique().to_list())
