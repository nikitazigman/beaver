import tomllib

from abc import ABC, abstractmethod
from pathlib import Path

from beaver_etl.schemas.extract_schema import InCodeSchema


class IPythonProjectParser(ABC):
    @abstractmethod
    def retrieve_data(self, project: Path) -> InCodeSchema:
        """Removes docstrings and comments from the code."""


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
        poetry_project_config = self.toml_to_dict(project)
        link_to_task = self.get_link_to_task(poetry_project_config)
        title = self.get_title(poetry_project_config)
        types = self.get_types(poetry_project_config)

        source_code = self.get_source_code(project)
        readme = self.get_readme(project)

        code_schema = InCodeSchema(
            source_code=source_code,
            link_to_task=link_to_task,
            title=title,
            types=types,
            language="python",
            readme=readme,
        )
        return code_schema

    def toml_to_dict(self, project: Path) -> dict:
        return tomllib.loads(
            (project / self.relative_path_to_pyproject_toml).read_text()
        )

    def get_link_to_task(self, poetry_config: dict) -> str:
        return poetry_config["tool"]["poetry"]["documentation"]

    def get_title(self, poetry_config: dict) -> str:
        return poetry_config["tool"]["poetry"]["description"]

    def get_types(self, poetry_config: dict) -> list[str]:
        return poetry_config["tool"]["poetry"]["keywords"]

    def get_source_code(self, project: Path) -> str:
        return (project / self.relative_path_to_main).read_text()

    def get_readme(self, project: Path) -> str:
        return (project / self.relative_path_to_readme).read_text()
