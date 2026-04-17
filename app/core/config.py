from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.engine import URL


class Settings(BaseSettings):
    redis_host: str
    redis_port: int
    redis_db: int
    redis_password: str

    @property
    def db_url(self):
        pass

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()