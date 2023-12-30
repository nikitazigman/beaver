from pydantic import BaseModel


class LoaderCodeSchema(BaseModel):
    source_code: str
    language: str
    link_to_task: str
    title: str
    types: list[str]
    readme: str
    hash: str
