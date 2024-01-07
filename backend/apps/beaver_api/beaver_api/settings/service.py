import multiprocessing

from beaver_api.settings.base import BaseAppSettings

import pydantic


class ServiceSettings(BaseAppSettings):

    api_host: str = pydantic.Field(default="127.0.0.1")

    api_port: int = pydantic.Field(default=8001)

    workers: int = pydantic.Field(default=multiprocessing.cpu_count() * 2 + 1)

    pidfile: str = pydantic.Field(default="/var/run/beaver_api.pid")

    unix_sock_path: str | None = pydantic.Field(default=None)

    def dsn(self) -> str:
        if self.unix_sock_path is not None:
            return self.unix_sock_path
        return f'{self.api_host}:{self.api_port}'
