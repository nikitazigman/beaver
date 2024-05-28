from pathlib import Path

from pydantic_settings import BaseSettings


ROOT_DIR = Path(__file__).resolve().parent.parent.parent.parent


class Settings(BaseSettings):
    path_to_dataset: Path = ROOT_DIR.joinpath("dataset").absolute()

    relative_path_to_main: str = "src/main.py"
    relative_path_to_pyproject_toml: str = "pyproject.toml"
    relative_path_to_readme: str = "README.md"

    service_url: str = "http://localhost:8000/"
