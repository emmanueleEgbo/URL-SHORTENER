"""Webhook delivery and CRUD service.

How it works end-to-end:
  1. A caller registers a webhook via create_webhook() — stores the target URL +
     the list of events it cares about.
  2. When something interesting happens (URL created, clicked, deleted) the route
     handler calls fire_event().
  3. fire_event() loads all active webhooks whose `events` list includes the
     current event, builds a JSON payload, and schedules an async HTTP POST to
     each target URL using asyncio.create_task() — so the delivery is completely
     non-blocking; the API response returns immediately.
"""
import asyncio
import logging
from datetime import datetime, timezone
from typing import List, Optional

import httpx
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.webhook import Webhook

logger = logging.getLogger(__name__)


# --------------------------------------------
# Internal helper functions
# --------------------------------------------

def _build_payment(event: str, data: dict) -> dict:
    return {
        "event": event,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "data": data,
    }


async def _deliver(webhook: Webhook, payload: dict) -> None:
    pass