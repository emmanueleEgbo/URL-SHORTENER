from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.engine import URL


class Settings(BaseSettings):
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_db: int = 0                # DB 0 -> URL cache (existing)
    redis_password: str | None

    database_url: str                # postgressql+asyncpg://...


    # Celery uses separate Redis DBs to avoid key collisions with the URL cache
    celery_broker_db: int = 1 # DB 1 -> Task queue
    celery_backend_db: int = 2 # task results

    model_config = SettingsConfigDict(env_file=".env")

    @property
    def redis_url(self) -> str:
        auth = f":{self.redis_password}@" if self.redis_password else ""
        return f"redis://{auth}{self.redis_host}:{self.redis_port}"
    
    @property
    def celery_broker_url(self) -> str:
        return f"{self.redis_url}/{self.celery_broker_db}"
    
    @property
    def celery_backend_url(self) -> str:
        return f"{self.redis_url}/{self.celery_backend_db}"




settings = Settings()