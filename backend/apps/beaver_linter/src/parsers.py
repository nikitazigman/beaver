import tomllib

from abc import ABC, abstractmethod
from pathlib import Path

from src.schemas import ParserCodeSchema
from src.settings import get_settings


class IParser(ABC):
    @abstractmethod
    def parse(self, project: Path) -> ParserCodeSchema:
        """retrieves data from a python project"""


class PoetryProjectParser(IParser):
    def __init__(
        self,
        path_to_main: str,
        path_to_pyproject_toml: str,
    ):
        self.path_to_main = path_to_main
        self.path_to_pyproject_toml = path_to_pyproject_toml
        self.settings = get_settings()

    def parse(self, project: Path) -> ParserCodeSchema:
        poetry_project_config = self._toml_to_dict(project)
        link_to_task = self._get_link_to_task(poetry_project_config)
        title = self._get_title(poetry_project_config)
        types = self._get_types(poetry_project_config)

        code_schema = ParserCodeSchema(
            link_to_project=link_to_task,
            title=title,
            tags=types,
            language="python",
            path=str(
                project.relative_to(self.settings.path_to_dataset.parent)
                / self.path_to_main
            ),
        )
        return code_schema

    def _toml_to_dict(self, project: Path) -> dict:
        return tomllib.loads(
            (project / self.path_to_pyproject_toml).read_text()
        )

    def _get_link_to_task(self, poetry_config: dict) -> str:
        print(poetry_config)
        return poetry_config["tool"]["poetry"]["documentation"]

    def _get_title(self, poetry_config: dict) -> str:
        return poetry_config["tool"]["poetry"]["description"]

    def _get_types(self, poetry_config: dict) -> list[str]:
        return poetry_config["tool"]["poetry"]["keywords"]


def get_parser(
    path_to_main: str,
    path_to_pyproject_toml: str,
) -> IParser:
    return PoetryProjectParser(path_to_main, path_to_pyproject_toml)
