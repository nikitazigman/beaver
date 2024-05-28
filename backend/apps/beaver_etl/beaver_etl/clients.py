from abc import ABC, abstractmethod

from beaver_etl.schemas import ParserCodeSchema


class IClient(ABC):
    @abstractmethod
    def send(self, code_schema: list[ParserCodeSchema]) -> None:
        "Send data to the API"


class BeaverAPI(IClient):
    def __init__(self, api_url: str) -> None:
        self.api_url = api_url

    # TODO: implement the send method
    def send(self, code_schema: list[ParserCodeSchema]) -> None:
        print(f"Sending data to {self.api_url}")

        for schema in code_schema:
            print(schema.model_dump_json(exclude={"readme", "source_code"}))


def get_client(api_url: str) -> IClient:
    return BeaverAPI(api_url=api_url)
