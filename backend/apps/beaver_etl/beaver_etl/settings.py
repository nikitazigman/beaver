from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings


ROOT_DIR = Path(__file__).resolve().parent.parent.parent.parent.parent


class Settings(BaseSettings):
    path_to_dataset: Path = ROOT_DIR.joinpath("dataset").absolute()

    relative_path_to_main: str = "src/main.py"
    relative_path_to_pyproject_toml: str = "pyproject.toml"
    relative_path_to_readme: str = "README.md"

    service_url: str = "http://localhost:8000"
    chunk_size: int = 10

    api_secret_token: str = "73092d292062a7cf2476d56770064c5d88b063d8"


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
