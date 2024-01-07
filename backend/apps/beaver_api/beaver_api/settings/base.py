from pydantic_settings import BaseSettings


class BaseAppSettings(BaseSettings):

    class Config:
        extra = "allow"
