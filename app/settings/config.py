from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    loglevel: str = Field("INFO")


settings = Settings()
