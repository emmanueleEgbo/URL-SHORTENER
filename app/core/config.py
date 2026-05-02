from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.engine import URL


class Settings(BaseSettings):
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_db: int = 0                # DB 0 -> URL cache (existing)
    redis_password: str | None

    database_url: str                # postgressql+asyncpg://...

    model_config = SettingsConfigDict(env_file=".env")

    # Celery uses separate Redis DBs to avoid key collisions with the URL cache


settings = Settings()