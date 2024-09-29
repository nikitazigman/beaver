from abc import ABC
from pathlib import Path

from src.parsers import IParser
from src.utils import find_projects

import yaml


class IService(ABC):
    def process(self, path_dataset: Path) -> None:
        """iterate over projects in dataset and validate project structure"""


class Service(IService):
    def __init__(self, parser: IParser) -> None:
        self.parser = parser

    def process(self, path_dataset: Path) -> None:
        projects = find_projects(path=path_dataset, key_file="pyproject.toml")
        code_schemas = [self.parser.parse(project) for project in projects]
        with open(path_dataset.parent / "meta.beaver.yaml", "w") as f:
            yaml.dump_all(
                [code_schema.model_dump() for code_schema in code_schemas], f
            )


def get_service(parser: IParser) -> IService:
    return Service(parser=parser)
