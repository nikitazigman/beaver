from contextlib import suppress
from queue import Empty, Queue
from threading import Event, Thread
from types import TracebackType
from typing import Self

from beaver_cli.schemas.code_document import CodeDocument
from beaver_cli.schemas.language import Language
from beaver_cli.schemas.tags import Tag
from beaver_cli.settings.settings import Settings, get_settings

import requests

from requests import HTTPError, Response
from requests.adapters import HTTPAdapter, Retry
from requests.sessions import Session


settings: Settings = get_settings()


class BeaverAPIService:
    def __init__(self, queue: Queue) -> None:
        self.queue: Queue = queue
        self.session = requests.Session()
        retries = Retry(total=5, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
        http_adapter = HTTPAdapter(max_retries=retries)
        self.session.mount(prefix="https://", adapter=http_adapter)

        self.code_api: CodeAPI = CodeAPI(session=self.session)
        self.language_api: LanguageAPI = LanguageAPI(session=self.session)
        self.tag_api: TagAPI = TagAPI(session=self.session)

        self.selected_tags: list[str] = []
        self.selected_language: str | None = None

        self._running: Event = Event()

        self.thread = Thread(target=self._background_task)

    def set_settings(self, tags: list[str], language: str | None) -> None:
        self.selected_tags = tags
        self.selected_language = language
        self._clear_queue()

    def get_all_languages(self) -> list[Language]:
        return self.language_api.get_all_languages()

    def get_all_tags(self) -> list[Tag]:
        return self.tag_api.get_all_tags()

    def get_code_document(self) -> CodeDocument | None:
        return self.queue.get(timeout=1)  # 1 sec timeout

    def _clear_queue(self) -> None:
        with suppress(Empty):
            while True:
                self.queue.get_nowait()

    def _background_task(self) -> None:
        while self._running.is_set():
            doc: CodeDocument | None = None

            with suppress(HTTPError):
                doc = self.code_api.get_code_document(tags=self.selected_tags, language=self.selected_language)

            self.queue.put(item=doc)

    def __enter__(self) -> Self:
        self._running.set()
        self.thread.start()

        return self

    def __exit__(self, exc_type: type[Exception], exc_value: Exception, traceback: TracebackType) -> None:
        self._running.clear()
        self._clear_queue()
        self.thread.join()
        self.session.close()


class CodeAPI:
    resource_path: str = f"{settings.service_url}/api/v1/code_documents/code_document/"

    def __init__(self, session: Session) -> None:
        self.session: Session = session

    def get_code_document(self, tags: list[str], language: str | None = None) -> CodeDocument:
        params: list[tuple[str, str]] = [("tags", tag) for tag in tags]

        if language:
            params.append(("language", language))

        response: Response = self.session.get(url=self.resource_path, params=params, timeout=5)

        response.raise_for_status()
        return CodeDocument.model_validate_json(json_data=response.text)


class LanguageAPI:
    resource_path: str = f"{settings.service_url}/api/v1/languages/"

    def __init__(self, session: Session) -> None:
        self.session: Session = session

    def get_all_languages(self) -> list[Language]:
        response: Response = self.session.get(url=self.resource_path)
        response.raise_for_status()

        languages_data: list[dict] = response.json()["results"]
        return [Language.model_validate(obj=language) for language in languages_data]


class TagAPI:
    resource_path: str = f"{settings.service_url}/api/v1/tags/"

    def __init__(self, session: Session) -> None:
        self.session: Session = session

    def get_all_tags(
        self,
    ) -> list[Tag]:
        response: Response = self.session.get(url=self.resource_path)
        response.raise_for_status()

        tag_data: list[dict] = response.json()["results"]
        return [Tag.model_validate(obj=tag) for tag in tag_data]
