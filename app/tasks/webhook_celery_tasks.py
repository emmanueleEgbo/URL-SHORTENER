"""Celery task: deliver a webhook payload to a single endpoint.

Replaces the asyncio.create_task(_deliver(...)) approach in webhook_service.py.
Key improvements over the old approach:
  - Survives worker restarts (task is re-queued if the worker dies mid-flight)
  - Automatic retry with exponential back-off on network / timeout errors
  - Visible in Flower (task state, retries, timing)
"""

import logging
import httpx
from app.celery_app import celery_app
from app.models.webhook import Webhook
from app.tasks.db import get_sync_db

logger = logging.getLogger(__name__)
