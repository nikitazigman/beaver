from pydantic import BaseModel


class PagePagination[T](BaseModel):
    count: int
    next: str
    previous: str
    results: list[T]
