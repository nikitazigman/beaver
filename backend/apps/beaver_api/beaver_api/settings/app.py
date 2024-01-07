from functools import lru_cache

from beaver_api.settings.base import BaseAppSettings
from beaver_api.settings.code_environment import CodeEnvironment
from beaver_api.settings.logging import LoggingSettings
from beaver_api.settings.service import ServiceSettings

import pydantic


class AppSettings(BaseAppSettings):

    environment: CodeEnvironment = pydantic.Field(default=CodeEnvironment.DEV)
    service_settings: ServiceSettings = ServiceSettings()
    logging: LoggingSettings = LoggingSettings()

    def is_development(self) -> bool:
        return self.environment == CodeEnvironment.DEV


@lru_cache(maxsize=1)
def get_app_settings():
    return AppSettings()
