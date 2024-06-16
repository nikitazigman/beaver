from abc import ABC, abstractmethod
from datetime import datetime
from types import TracebackType
from typing import Self

import requests

from beaver_etl.schemas import DeleteSchemaOut, UpdateCodeSchemaOut
from requests.adapters import HTTPAdapter, Retry


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

    def __init__(self, api_url: str) -> None:
        self.base_url = f"{api_url}/{self.api_version}{self.resource_path}"

    def start_session(self) -> None:
        retries = Retry(
            total=5,
            backoff_factor=1,
            status_forcelist=[400, 500, 502, 503, 504],
        )
        http_adapter = HTTPAdapter(max_retries=retries)
        self.session = requests.Session()
        self.session.mount("http://", http_adapter)

    def close_session(self) -> None:
        self.session.close()

    def __enter__(self) -> IClient:
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
        response = self.session.post(resource_url, json=data_out)
        response.raise_for_status()

    def delete(self, timestamp: datetime) -> None:
        data_out = DeleteSchemaOut(timestamp=str(timestamp))
        resource_url = f"{self.base_url}{self.delete_path}"
        response = self.session.post(resource_url, json=data_out.model_dump())
        response.raise_for_status()


def get_client(api_url: str) -> IClient:
    return BeaverAPI(api_url=api_url)
