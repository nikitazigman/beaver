from abc import ABC
from datetime import UTC, datetime
from pathlib import Path

from schemas import ParserCodeSchema
from src.clients import IClient
from src.parsers import IParser
from src.schemas import UpdateCodeSchemaOut
from src.utils import chunked, find_projects


class IService(ABC):
    def process(self, path_dataset: Path, chunk_size: int) -> None:
        """iterate over projects in dataset and send update to the API"""


class Service(IService):
    def __init__(self, parser: IParser, client: IClient, beaver_file: str) -> None:
        self.parser: IParser = parser
        self.client: IClient = client
        self.beaver_file: str = beaver_file

    def transform_schema(self, code_schema: ParserCodeSchema, timestamp: datetime) -> UpdateCodeSchemaOut:
        contributors: list[dict[str, str]] = [
            {
                "name": contributor.name,
                "last_name": contributor.last_name,
                "address": contributor.email,
            }
            for contributor in code_schema.contributors
        ]

        return UpdateCodeSchemaOut(
            last_synchronization=str(object=timestamp),
            title=code_schema.title,
            code=code_schema.code,
            link_to_project=code_schema.link_to_project,
            language=code_schema.language,
            tags=code_schema.tags,
            contributors=contributors,  # type: ignore
        )

    def process(self, path_dataset: Path, chunk_size: int) -> None:
        timestamp: datetime = datetime.now(tz=UTC)
        projects: list[Path] = find_projects(path=path_dataset, key_file=self.beaver_file)

        with self.client as client:
            for chunk in chunked(iterable=projects, chunk_size=chunk_size):
                parsed_schemas: list[ParserCodeSchema] = [self.parser.parse(project=project) for project in chunk]

                code_schemas: list[UpdateCodeSchemaOut] = [
                    self.transform_schema(code_schema=schema, timestamp=timestamp) for schema in parsed_schemas
                ]

                client.send(code_schema=code_schemas)

            client.delete(timestamp=timestamp)


def get_service(parser: IParser, client: IClient, beaver_file: str) -> IService:
    return Service(parser=parser, client=client, beaver_file=beaver_file)
