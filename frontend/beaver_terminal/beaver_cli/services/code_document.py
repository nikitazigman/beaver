from abc import ABC, abstractmethod

from beaver_cli.schemas.code_document import CodeDocument
from beaver_cli.settings.settings import get_settings

from requests.sessions import Session


settings = get_settings()


class ICodeService(ABC):
    @abstractmethod
    def get_code_document(self, tag_name: str, language: str) -> CodeDocument:
        "Get a random code document"


class CodeService(ICodeService):
    resource_path = (
        f"{settings.service_url}/api/v1/code_documents/code_document/"
    )

    def __init__(self, session: Session) -> None:
        self.session = session

    def get_code_document(
        self, tag_name: str = "", language: str = ""
    ) -> CodeDocument:
        response = self.session.get(
            self.resource_path,
            params={"tag_name": tag_name, "language": language},
        )
        response.raise_for_status()
        return CodeDocument.model_validate_json(response.text)
