from celery import Celery
from celery.schedules import crontab
from app.core.config import settings


def create_celery_app() -> Celery:
    app = Celery(
        "url_shortener",
        broker=settings.celery_broker_url,
        backend=settings.celery_backend_url,
        include=[

        ],
    )