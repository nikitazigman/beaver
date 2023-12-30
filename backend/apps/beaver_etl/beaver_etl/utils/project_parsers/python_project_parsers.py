import tomllib

from abc import ABC, abstractmethod
from pathlib import Path

from backend.apps.beaver_etl.beaver_etl.schemas.parser import InCodeSchema


class IPythonProjectParser(ABC):
    @abstractmethod
    def retrieve_data(self, project: Path) -> InCodeSchema:
        """retrieves data from a python project"""


class PoetryProjectParser(IPythonProjectParser):
    def __init__(
        self,
        relative_path_to_main: str = "src/main.py",
        relative_path_to_pyproject_toml: str = "pyproject.toml",
        relative_path_to_readme: str = "README.md",
    ):
        self.relative_path_to_main = relative_path_to_main
        self.relative_path_to_pyproject_toml = relative_path_to_pyproject_toml
        self.relative_path_to_readme = relative_path_to_readme

    def retrieve_data(self, project: Path) -> InCodeSchema:
        poetry_project_config = self._toml_to_dict(project)
        link_to_task = self._get_link_to_task(poetry_project_config)
        title = self._get_title(poetry_project_config)
        types = self._get_types(poetry_project_config)

        source_code = self._get_source_code(project)
        readme = self._get_readme(project)

        code_schema = InCodeSchema(
            source_code=source_code,
            link_to_task=link_to_task,
            title=title,
            types=types,
            language="python",
            readme=readme,
        )
        return code_schema

    def _toml_to_dict(self, project: Path) -> dict:
        return tomllib.loads(
            (project / self.relative_path_to_pyproject_toml).read_text()
        )

    def _get_link_to_task(self, poetry_config: dict) -> str:
        return poetry_config["tool"]["poetry"]["documentation"]

    def _get_title(self, poetry_config: dict) -> str:
        return poetry_config["tool"]["poetry"]["description"]

    def _get_types(self, poetry_config: dict) -> list[str]:
        return poetry_config["tool"]["poetry"]["keywords"]

    def _get_source_code(self, project: Path) -> str:
        return (project / self.relative_path_to_main).read_text()

    def _get_readme(self, project: Path) -> str:
        return (project / self.relative_path_to_readme).read_text()
