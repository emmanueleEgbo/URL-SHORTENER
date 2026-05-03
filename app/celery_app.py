from celery import Celery
from celery.schedules import crontab
from app.core.config import settings


def create_celery_app() -> Celery:
    pass