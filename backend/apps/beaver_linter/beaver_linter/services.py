from abc import ABC
from pathlib import Path

from beaver_linter.parsers import IParser
from beaver_linter.utils import find_projects


class IService(ABC):
    def process(self, path_dataset: Path) -> None:
        """iterate over projects in dataset and validate project structure"""


class Service(IService):
    def __init__(self, parser: IParser) -> None:
        self.parser = parser

    def process(self, path_dataset: Path) -> None:
        projects = find_projects(path=path_dataset, key_file="pyproject.toml")
        [self.parser.parse(project) for project in projects]


def get_service(parser: IParser) -> IService:
    return Service(parser=parser)
