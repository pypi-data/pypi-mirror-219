from enum import Enum


class PowerBiAsset(Enum):
    """PowerBi assets"""

    DASHBOARDS = "dashboards"
    DATASETS = "datasets"
    DATASET_FIELDS = "dataset_fields"
    METADATA = "metadata"
    REPORTS = "reports"
    TABLES = "tables"
    USERS = "users"


class MetadataAsset(Enum):
    """
    Assets extracted from the Metadata file, they are not directly fetch
    from the PowerBi api.
    """

    USERS = "users"
    TABLES = "tables"
