from abc import ABC, abstractmethod

from beaver_cli.schemas.code_document import CodeDocument
from beaver_cli.settings.settings import get_settings

from requests import HTTPError
from requests.sessions import Session


settings = get_settings()


class ICodeService(ABC):
    @abstractmethod
    def get_code_document(self, tags: list[str] | None = None, language: str | None = None) -> CodeDocument:
        "Get a random code document"


class CodeService(ICodeService):
    resource_path = f"{settings.service_url}/api/v1/code_documents/code_document/"

    def __init__(self, session: Session) -> None:
        self.session = session

    def get_code_document(self, tags: list[str] | None = None, language: str | None = None) -> CodeDocument:
        params = []

        if tags:
            for tag in tags:
                params.append(("tags", tag))

        if language:
            params.append(("language", language))

        try:
            response = self.session.get(
                self.resource_path,
                params=params,
                timeout=5,
            )

            response.raise_for_status()
            return CodeDocument.model_validate_json(response.text)

        except HTTPError as e:
            if e.response.status_code == 404:
                raise FileNotFoundError(
                    "The requested code document could not be found. "
                    "Please try a different combination of tags or language, "
                    "as the specified document may not yet exist in the database."
                )
            else:
                raise ConnectionError(f"An error occurred while fetching the code document: {e}")

        except Exception as e:
            raise ConnectionError(f"An unexpected error occurred while fetching the code document: {e}")
