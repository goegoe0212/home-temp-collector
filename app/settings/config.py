from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    loglevel: str = Field("INFO")
    nature_api_key: str = Field(default="sample_api_key")
    nature_device_name: str = Field(default="Remo")
    postgresql_host: str = Field(default="192.168.20.102")
    postgresql_port: int = Field(default=5432)
    postgresql_dbname: str = Field(default="postgresdb")
    postgresql_user: str = Field(default="admin")
    postgresql_password: str = Field(default="Passw0rd")


settings = Settings()
