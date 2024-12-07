from beaver_cli.schemas.tags import Tag
from beaver_cli.settings.settings import Settings, get_settings

from requests import Response
from requests.sessions import Session


settings: Settings = get_settings()


class TagService:
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
