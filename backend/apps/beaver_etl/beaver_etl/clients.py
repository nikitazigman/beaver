from abc import ABC, abstractmethod
from types import TracebackType

import requests

from beaver_etl.schemas import ParserCodeSchema
from requests.adapters import HTTPAdapter, Retry


class IClient(ABC):
    @abstractmethod
    def send(self, code_schema: list[ParserCodeSchema]) -> None:
        "Send data to the API"

    @abstractmethod
    def __enter__(self):
        "Enter the context manager"

    @abstractmethod
    def __exit__(
        self,
        exc_type: type[Exception],
        exc_value: Exception,
        traceback: TracebackType,
    ):
        "Exit the context manager"


class BeaverAPI(IClient):
    resource = "code"

    def __init__(self, api_url: str) -> None:
        self.base_url = api_url

    def start_session(self) -> None:
        retries = Retry(
            total=5,
            backoff_factor=1,
            status_forcelist=[400, 500, 502, 503, 504],
        )
        http_adapter = HTTPAdapter(max_retries=retries)
        self.session = requests.Session()
        self.session.mount("https://", http_adapter)

    def close_session(self) -> None:
        self.session.close()

    def __enter__(self) -> IClient:
        return self

    def __exit__(
        self,
        exc_type: type[Exception],
        exc_value: Exception,
        traceback: TracebackType,
    ) -> None:
        self.close_session()

    def send(self, code_schema: list[ParserCodeSchema]) -> None:
        resource_url = f"{self.base_url}/{self.resource}"
        self.session.post(resource_url, json=code_schema)


def get_client(api_url: str) -> IClient:
    return BeaverAPI(api_url=api_url)
