from abc import ABC, abstractmethod

from beaver_etl.schemas import ParserCodeSchema


class IClient(ABC):
    @abstractmethod
    def send(self, code_schema: list[ParserCodeSchema]) -> None:
        "Send data to the API"


class BeaverAPI(IClient):
    def __init__(self, api_url: str) -> None:
        self.api_url = api_url

    def send(self, code_schema: list[ParserCodeSchema]) -> None:
        ...


def get_client(api_url: str) -> IClient:
    return BeaverAPI(api_url=api_url)
