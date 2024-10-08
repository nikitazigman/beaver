from typing import Annotated

from pydantic import BaseModel
from pydantic.functional_validators import AfterValidator


def not_empty(value: str) -> str:
    if not value:
        raise ValueError("field cannot be empty")

    return value


NonEmptyStr = Annotated[str, AfterValidator(not_empty)]


class ParserCodeSchema(BaseModel):
    title: NonEmptyStr
    link_to_project: NonEmptyStr
    language: NonEmptyStr
    tags: list[NonEmptyStr]
    path: NonEmptyStr
