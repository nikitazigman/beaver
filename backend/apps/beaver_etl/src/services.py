from abc import ABC
from datetime import UTC, datetime
from pathlib import Path

from src.clients import IClient
from src.parsers import IParser
from src.schemas import UpdateCodeSchemaOut
from src.utils import chunked, find_projects


class IService(ABC):
    def process(self, path_dataset: Path, chunk_size: int) -> None:
        """iterate over projects in dataset and send update to the API"""


class Service(IService):
    def __init__(self, parser: IParser, client: IClient) -> None:
        self.parser = parser
        self.client = client

    def process(self, path_dataset: Path, chunk_size: int) -> None:
        timestamp = datetime.now(tz=UTC)
        projects = find_projects(path=path_dataset, key_file="pyproject.toml")

        with self.client as client:
            for chunk in chunked(projects, chunk_size):
                parsed_schemas = [
                    self.parser.parse(project) for project in chunk
                ]
                code_schemas = [
                    UpdateCodeSchemaOut.model_validate(
                        {
                            "last_synchronization": str(timestamp),
                            **schema.model_dump(),
                        }
                    )
                    for schema in parsed_schemas
                ]

                client.send(code_schemas)

            client.delete(timestamp)


def get_service(parser: IParser, client: IClient) -> IService:
    return Service(parser=parser, client=client)
