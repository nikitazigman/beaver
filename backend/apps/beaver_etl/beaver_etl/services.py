from abc import ABC
from pathlib import Path

from beaver_etl.clients import IClient
from beaver_etl.parsers import IParser
from beaver_etl.utils import chunked, find_projects


class IService(ABC):
    def process(self, path_dataset: Path) -> None:
        """iterate over projects in dataset and send update to the API"""


class Service(IService):
    def __init__(self, parser: IParser, client: IClient) -> None:
        self.parser = parser
        self.client = client

    def process(self, path_dataset: Path, chunk_size: int) -> None:
        projects = find_projects(path=path_dataset, key_file="pyproject.toml")
        code_schemas = [self.parser.parse(project) for project in projects]

        for chunk in chunked(code_schemas, chunk_size):
            self.client.send(chunk)


def get_service(parser: IParser, client: IClient) -> IService:
    return Service(parser=parser, client=client)
