from abc import ABC, abstractmethod

from beaver_cli.schemas.tags import Tag
from beaver_cli.settings.settings import get_settings

from requests.sessions import Session


settings = get_settings()


class ITagService(ABC):
    @abstractmethod
    def get_all_tags() -> list[Tag]:
        "Get all tags"


class TagService(ITagService):
    resource_path = (
        f"{settings.service_url}/api/v1/tags/"
    )

    def __init__(self, session: Session) -> None:
        self.session = session

    def get_all_tags(
        self,
    ) -> Tag:
        response = self.session.get(
            self.resource_path,
        )
        response.raise_for_status()

        tag_data = response.json()["results"]
        return [Tag.model_validate(tag) for tag in tag_data]
