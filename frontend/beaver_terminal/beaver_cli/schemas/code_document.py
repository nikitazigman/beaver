from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class CodeDocument(BaseModel):
    id: UUID
    title: str
    code: str
    tags: list[str]
    language: str
    link_to_project: str

    updated_at: datetime
    created_at: datetime
