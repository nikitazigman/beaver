from beaver_cli.schemas.language import Language
from beaver_cli.settings.settings import Settings, get_settings

from requests import Response
from requests.sessions import Session


settings: Settings = get_settings()


class LanguageService:
    resource_path: str = f"{settings.service_url}/api/v1/languages/"

    def __init__(self, session: Session) -> None:
        self.session: Session = session

    def get_all_languages(self) -> list[Language]:
        response: Response = self.session.get(url=self.resource_path)
        response.raise_for_status()

        languages_data: list[dict] = response.json()["results"]
        return [Language.model_validate(obj=language) for language in languages_data]
