from pydantic import BaseModel


class ParserCodeSchema(BaseModel):
    source_code: str
    language: str
    link: str
    title: str
    types: list[str]
    readme: str
