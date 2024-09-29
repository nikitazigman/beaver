from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings


ROOT_DIR = Path(__file__).resolve().parent.parent.parent.parent.parent


class Settings(BaseSettings):
    path_to_dataset: Path = ROOT_DIR.joinpath(
        "dataset/python/algorithms"
    ).absolute()

    relative_path_to_main: str = "./main.py"
    relative_path_to_pyproject_toml: str = "pyproject.toml"
    chunk_size: int = 10


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
