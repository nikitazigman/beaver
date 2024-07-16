from pydantic import BaseModel


class Statistic(BaseModel):
    typing_errors: list[float]
    typing_events: list[float]
