from pathlib import Path
from typing import Annotated

from pydantic.functional_validators import AfterValidator
from pydantic.main import BaseModel


def not_empty(value: str) -> str:
    if not value:
        raise ValueError("field cannot be empty")

    return value


NonEmptyStr = Annotated[str, AfterValidator(not_empty)]
BEAVER_FILE = "beaver.json"
ROOT_DIR = Path(__file__).resolve().parent.parent.parent.parent.parent
PATH_TO_DATASET: Path = ROOT_DIR.joinpath("dataset").absolute()
PATH_TO_PYTHON_PROJECTS: Path = PATH_TO_DATASET.joinpath("python")


class Author(BaseModel):
    name: NonEmptyStr
    last_name: NonEmptyStr
    email: NonEmptyStr


class BeaverCodeSchema(BaseModel):
    title: NonEmptyStr
    link_to_project: NonEmptyStr
    language: NonEmptyStr
    tags: list[NonEmptyStr]
    path: NonEmptyStr
    authors: list[Author]


def find_projects(path: Path, key_file: str) -> list[Path]:
    projects_paths: list[Path] = []

    def _recursion(path: Path) -> None:
        if path.joinpath(key_file).exists():
            projects_paths.append(path)
            return

        for project in path.iterdir():
            if project.is_dir():
                _recursion(project)

    _recursion(path)

    return projects_paths


def python_checker(project: Path) -> None:
    with project.joinpath(BEAVER_FILE).open() as file:
        content = BeaverCodeSchema.model_validate_json(file.read())

    path_to_code = PATH_TO_DATASET.joinpath(content.path)

    if not path_to_code.is_file():
        raise FileNotFoundError(f"File {path_to_code} not found")


def main() -> None:
    for python_project_path in find_projects(
        path=PATH_TO_PYTHON_PROJECTS,
        key_file=BEAVER_FILE,
    ):
        python_checker(python_project_path)


if __name__ == "__main__":
    main()
