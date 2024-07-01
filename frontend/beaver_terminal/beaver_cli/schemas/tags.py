from uuid import UUID

from pydantic import BaseModel


class Tag(BaseModel):
    id: UUID
    name: str
