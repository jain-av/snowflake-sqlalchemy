from enum import Enum


class SnowflakeKeyword(Enum):
    # TARGET_LAG
    DOWNSTREAM = "DOWNSTREAM"

    # REFRESH_MODE
    AUTO = "AUTO"
    FULL = "FULL"
    INCREMENTAL = "INCREMENTAL"
