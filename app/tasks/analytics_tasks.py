"""Periodic Celery tasks for analytics and housekeeping.

Both tasks are registered in the beat_schedule inside celery_app.py:
  - daily_analytics_rollup  → midnight UTC every day
  - cleanup_expired_links   → every hour on the hour
"""

import logging 
from app.celery_app import celery_app
from app.models.url_model import URL
from app.tasks.db import get_sync_db

logger = logging.getLogger(__name__)


@celery_app.task(name="app.tasks.analytics_tasks.daily_analytics_rollup")
def daily_analytics_rollup() -> None:
    """Log a daily summary of URLs stored in the system.

    This is intentionally simple for now — a future iteration can write
    aggregated click counts to a dedicated analytics table once a clicks
    column (or separate clicks model) is in place.
    """
    with get_sync_db as db:
        total = db.query(URL).count()

    logger.info("Daily analytics rollup: %d total short URLs in system", total)