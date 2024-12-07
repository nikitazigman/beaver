from beaver_cli.schemas.code_document import CodeDocument
from beaver_cli.settings.settings import get_settings

from requests import HTTPError, Response
from requests.sessions import Session


settings = get_settings()


class CodeService:
    resource_path: str = f"{settings.service_url}/api/v1/code_documents/code_document/"

    def __init__(self, session: Session) -> None:
        self.session: Session = session

    def get_code_document(self, tags: list[str] | None = None, language: str | None = None) -> CodeDocument:
        tags = tags or []

        params: list[tuple[str, str]] = [("tags", tag) for tag in tags]

        if language:
            params.append(("language", language))

        try:
            response: Response = self.session.get(url=self.resource_path, params=params, timeout=5)

            response.raise_for_status()
            return CodeDocument.model_validate_json(json_data=response.text)

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
