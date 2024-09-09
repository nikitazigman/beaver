from abc import ABC, abstractmethod

from beaver_cli.schemas.language import Language
from beaver_cli.settings.settings import get_settings

from requests.sessions import Session


settings = get_settings()


class ILanguageService(ABC):
    @abstractmethod
    def get_all_languages() -> list[Language]:
        "Get all languages"


class LanguageService(ILanguageService):
    resource_path = (
        f"{settings.service_url}/api/v1/languages/"
    )

    def __init__(self, session: Session) -> None:
        self.session = session

    def get_all_languages(
        self,
    ) -> Language:
        response = self.session.get(
            self.resource_path,
        )
        response.raise_for_status()

        languages_data = response.json()["results"]
        return [Language.model_validate(language) for language in languages_data]
