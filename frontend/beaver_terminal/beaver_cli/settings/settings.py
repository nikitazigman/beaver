from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    service_url: str = "https://beaver-api.com"


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
