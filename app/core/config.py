from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.engine import URL


class Settings(BaseSettings):
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_db: int = 0
    redis_password: str | None

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()