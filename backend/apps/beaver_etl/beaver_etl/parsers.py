import tomllib

from abc import ABC, abstractmethod
from pathlib import Path

from beaver_etl.schemas import ParserCodeSchema


class IParser(ABC):
    @abstractmethod
    def parse(self, project: Path) -> ParserCodeSchema:
        """retrieves data from a python project"""


class PoetryProjectParser(IParser):
    def __init__(
        self,
        path_to_main: str,
        path_to_pyproject_toml: str,
        path_to_readme: str,
    ):
        self.path_to_main = path_to_main
        self.path_to_pyproject_toml = path_to_pyproject_toml
        self.path_to_readme = path_to_readme

    def parse(self, project: Path) -> ParserCodeSchema:
        poetry_project_config = self._toml_to_dict(project)
        link_to_task = self._get_link_to_task(poetry_project_config)
        title = self._get_title(poetry_project_config)
        types = self._get_types(poetry_project_config)

        source_code = self._get_source_code(project)
        readme = self._get_readme(project)

        code_schema = ParserCodeSchema(
            code=source_code,
            link_to_project=link_to_task,
            title=title,
            tags=types,
            language="python",
            readme=readme,
        )
        return code_schema

    def _toml_to_dict(self, project: Path) -> dict:
        return tomllib.loads(
            (project / self.path_to_pyproject_toml).read_text()
        )

    def _get_link_to_task(self, poetry_config: dict) -> str:
        return poetry_config["tool"]["poetry"]["documentation"]

    def _get_title(self, poetry_config: dict) -> str:
        return poetry_config["tool"]["poetry"]["description"]

    def _get_types(self, poetry_config: dict) -> list[str]:
        return poetry_config["tool"]["poetry"]["keywords"]

    def _get_source_code(self, project: Path) -> str:
        return (project / self.path_to_main).read_text()

    def _get_readme(self, project: Path) -> str:
        return (project / self.path_to_readme).read_text()


def get_parser(
    path_to_main: str,
    path_to_pyproject_toml: str,
    path_to_readme: str,
) -> IParser:
    return PoetryProjectParser(
        path_to_main, path_to_pyproject_toml, path_to_readme
    )
