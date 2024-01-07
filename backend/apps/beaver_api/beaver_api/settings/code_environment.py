from enum import Enum, unique


@unique
class CodeEnvironment(str, Enum):
    CI: str = "CI"
    DEV: str = "DEV"
    PROD: str = "PROD"
