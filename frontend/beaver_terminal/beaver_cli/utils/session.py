from abc import ABC, abstractmethod
from types import TracebackType

import requests

from requests.adapters import HTTPAdapter, Retry


class ISession(ABC):
    @abstractmethod
    def __enter__(self) -> requests.Session:
        "Enter the context manager"

    @abstractmethod
    def __exit__(
        self,
        exc_type: type[Exception],
        exc_value: Exception,
        traceback: TracebackType,
    ) -> None:
        "Exit the context manager"


class Session(ISession):
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

    def __enter__(self) -> requests.Session:
        self.start_session()
        return self.session

    def __exit__(
        self,
        exc_type: type[Exception],
        exc_value: Exception,
        traceback: TracebackType,
    ) -> None:
        self.close_session()
