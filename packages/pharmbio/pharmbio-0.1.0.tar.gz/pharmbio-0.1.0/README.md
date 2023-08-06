# pharmbio (Python package)
A Python package automating routine pharmaceutical bioinformatics laboratory analyses and quality control checks.

This is a Python package for interacting with Pharmbio databases. 

## Installation

You can install this package from PyPI:

```sh
pip install pharmbio
```

## Usage

Here's an example of how you can use this package:

```py
from pharmbio.dataset import ExperimentData

experiment = ExperimentData(
    name="experiment_name",
    drop_replication="Auto",
    keep_replication="None",
    filter=None,
)
```

Please refer to the [documentation](https://pharmbio.github.io/pharmbio_package/) for more information.
