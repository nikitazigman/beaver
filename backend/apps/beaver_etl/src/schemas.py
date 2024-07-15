from pydantic import BaseModel


class ParserCodeSchema(BaseModel):
    title: str
    code: str
    link_to_project: str
    language: str
    tags: list[str]


class DeleteSchemaOut(BaseModel):
    timestamp: str


class UpdateCodeSchemaOut(BaseModel):
    title: str
    code: str
    link_to_project: str
    language: str
    tags: list[str]
    last_synchronization: str
