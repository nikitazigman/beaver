from pydantic import BaseModel


class ContributorSchema(BaseModel):
    name: str
    last_name: str
    email: str


class InfoCodeSchema(BaseModel):
    title: str
    link_to_project: str
    language: str
    tags: list[str]
    contributors: list[ContributorSchema]
    path: str


class ParserCodeSchema(BaseModel):
    title: str
    code: str
    link_to_project: str
    language: str
    contributors: list[ContributorSchema]
    tags: list[str]


class DeleteSchemaOut(BaseModel):
    timestamp: str


class ContributorSchemaOut(BaseModel):
    name: str
    last_name: str
    address: str


class UpdateCodeSchemaOut(BaseModel):
    title: str
    code: str
    link_to_project: str
    language: str
    tags: list[str]
    contributors: list[ContributorSchemaOut]
    last_synchronization: str
