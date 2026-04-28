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

def _build_payload(event: str, data: dict) -> dict:
    return {
        "event": event,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "data": data,
    }


async def _deliver(webhook: Webhook, payload: dict) -> None:
    """POST the payload to a single webhook URL. Errors are logged, never raised."""
    headers = {
        "Content-Type": "application/json",
        "X-Webhook-Event": payload["event"],
        "User-Agent": "URLShortener-Webhook/1.0",
    }

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(webhook.url, json=payload, headers=headers)
            logger.info("Webhook %s -> %s status=%s", webhook.id, webhook.url, response.status_code)
    except Exception as e:
        logger.error("Webhook %s deliver failed to %s: %s", webhook.id, webhook.url, e)


# --------------------------------------------
# Public: event firing
# --------------------------------------------

async def fire_event(db: AsyncSession, event: str, data: dict) -> None:
    """Fire `event` to every active webhook subscribed to it.

    Uses asyncio.create_task(), so delivery is fire-and-forget - the HTTP call 
    happens in the background and the API route returns without waiting.
    """
    result = await db.execute(select(Webhook).where(Webhook.is_active.is_(True)))
    webhooks: List[Webhook] = result.scalars().all()

    payload = _build_payload(event, data)

    for wh in webhooks:
        if event in (wh.events or []):
            # create_task schedules the coroutine on the running event loop
            # without blocking the current request
            asyncio.create_task(_deliver(wh, payload))


# --------------------------------------------
# Public: CRUD
# --------------------------------------------

async def create_webhook(
    db: AsyncSession,
    name: str,
    url: str,
    events: List[str],
) -> Webhook:
    wh = Webhook(name=name, url=url, events=events)
    db.add(wh)
    await db.commit()
    await db.refresh()
    return wh


async def get_all_webhooks(db: AsyncSession) -> List[Webhook]:
    result = await db.execute(select(Webhook))
    return result