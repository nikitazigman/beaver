from abc import ABC, abstractmethod
from datetime import datetime
from types import TracebackType
from typing import Self

import requests

from requests.adapters import HTTPAdapter, Retry
from src.schemas import DeleteSchemaOut, UpdateCodeSchemaOut


class IClient(ABC):
    @abstractmethod
    def send(self, code_schema: list[UpdateCodeSchemaOut]) -> None:
        "Synchronize data with the API"

    @abstractmethod
    def delete(self, timestamp: datetime) -> None:
        "Delete all code document updated before the timestamp"

    @abstractmethod
    def __enter__(self) -> Self:
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
    api_version = "api/v1/"
    resource_path = "code_documents/"
    update_path = "bulk_update/"
    delete_path = "bulk_delete/"

    def __init__(self, api_url: str, token: str) -> None:
        self.token = token
        self.base_url = f"{api_url}/{self.api_version}{self.resource_path}"

    def start_session(self) -> None:
        retries = Retry(
            total=5,
            backoff_factor=0.1,
            status_forcelist=[400, 500, 502, 503, 504],
            allowed_methods=["GET", "POST", "DELETE"],
        )
        http_adapter = HTTPAdapter(max_retries=retries, pool_maxsize=1)
        self.session = requests.Session()
        self.session.mount("https://", http_adapter)
        self.session.mount("http://", http_adapter)
        self.session.headers["Authorization"] = f"Token {self.token}"

    def close_session(self) -> None:
        self.session.close()

    def __enter__(self) -> Self:
        self.start_session()
        return self

    def __exit__(
        self,
        exc_type: type[Exception],
        exc_value: Exception,
        traceback: TracebackType,
    ) -> None:
        self.close_session()

    def send(self, code_schema: list[UpdateCodeSchemaOut]) -> None:
        resource_url = f"{self.base_url}{self.update_path}"
        data_out = [schema.model_dump() for schema in code_schema]
        try:
            self.session.post(resource_url, json=data_out)
        except requests.exceptions.RetryError:
            print([schema.title for schema in code_schema])

    def delete(self, timestamp: datetime) -> None:
        data_out = DeleteSchemaOut(timestamp=str(timestamp))
        resource_url = f"{self.base_url}{self.delete_path}"
        response = self.session.post(resource_url, json=data_out.model_dump())
        response.raise_for_status()


def get_client(api_url: str, token: str) -> IClient:
    return BeaverAPI(api_url=api_url, token=token)
