import logging
import os
import time

from enum import Enum, unique
from typing import Any

from beaver_api.settings.base import BaseAppSettings
from beaver_api.settings.code_environment import CodeEnvironment

import pydantic
import structlog


logging.Formatter.converter = time.gmtime


COMMON_FORMAT = "[%(asctime)s] [%(name)s] [%(levelname)s] [%(process)d] [%(message)s]"


@unique
class LoggerLevelType(str, Enum):
    CRITICAL: str = "CRITICAL"
    ERROR: str = "ERROR"
    WARNING: str = "WARNING"
    INFO: str = "INFO"
    DEBUG: str = "DEBUG"


def get_dev_config(log_level: LoggerLevelType, log_file_path: str) -> dict[str, Any]:
    config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "()": structlog.stdlib.ProcessorFormatter,
                "processor": structlog.processors.format_exc_info,
                "fmt": COMMON_FORMAT
            }
        },
        "handlers": {
            "console": {
                "level": LoggerLevelType.DEBUG.value,
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
                "formatter": "default"
            },
            "file": {
                "level": LoggerLevelType.DEBUG.value,
                "class": "logging.FileHandler",
                "mode": "a",
                "encoding": "UTF-8",
                "filename": log_file_path,
                "formatter": "default"
            }
        },
        "loggers": {
            "": {
                "handlers": ["console", "file"],
                "level": log_level.value
            }
        }
    }
    return config


def get_prod_config(log_level: LoggerLevelType) -> dict[str, Any]:
    config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "()": structlog.stdlib.ProcessorFormatter,
                "processor": structlog.processors.format_exc_info,
                "fmt": COMMON_FORMAT
            }
        },
        "handlers": {
            "console": {
                "level": LoggerLevelType.DEBUG.value,
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
                "formatter": "default"
            },
        },
        "loggers": {
            "": {
                "handlers": ["console"],
                "level": log_level.value
            },
            "gunicorn.error": {
                "level": log_level.value,
                "handlers": ["console"],
                "propagate": False,
                "qualname": "gunicorn.error"
            },
        }
    }
    return config


class LoggingSettings(BaseAppSettings):

    log_level: LoggerLevelType = pydantic.Field(default=LoggerLevelType.INFO)

    log_file_path: str = pydantic.Field(default=os.path.join(os.getcwd(), "logs", "beaver_api.logs"))

    def get_config(self, environment: CodeEnvironment = CodeEnvironment.DEV) -> dict[str, Any] | None:
        if environment == CodeEnvironment.DEV:
            return get_dev_config(self.log_level, self.log_file_path)
        elif environment == CodeEnvironment.PROD:
            return get_prod_config(self.log_level)
        return {}
