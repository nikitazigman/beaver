from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


SERVICE_ROOT = Path(__file__).resolve().parent.parent
REPOSITORY_ROOT = SERVICE_ROOT.parent.parent.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=SERVICE_ROOT / ".env", env_file_encoding="utf-8"
    )
    path_to_dataset: Path = REPOSITORY_ROOT.joinpath("dataset").absolute()

    relative_path_to_main: str = "src/main.py"
    relative_path_to_pyproject_toml: str = "pyproject.toml"
    relative_path_to_readme: str = "README.md"

    service_url: str = "https://beaver-api.com"
    chunk_size: int = 1

    api_secret_token: str


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()  # type: ignore
