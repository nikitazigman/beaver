from uuid import UUID

from pydantic import BaseModel


class Language(BaseModel):
    id: UUID
    name: str
