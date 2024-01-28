from pydantic import BaseModel


class ExtractorCodeSchema(BaseModel):
    source_code: str
    language: str
    link_to_task: str
    title: str
    types: set[str]
    readme: str
