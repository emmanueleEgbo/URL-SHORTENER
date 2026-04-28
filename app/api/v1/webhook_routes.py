from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.async_database import get_db
from app.schemas.webhooks_schema import WebhookCreate, WebhookResponse
from app.services import webhook_service


webhook_router = APIRouter(prefix="/v1/webhooks", tags=["webhooks"])


@webhook_router.post("", response_model=WebhookResponse, status_code=201)
async def register_webhook(body: WebhookCreate, db: AsyncSession = Depends(get_db)):
    """Register a new webhook endpoint.
    Tip: grab a free listener URL from https://webhook.site then paste it here.
    Your URL shortener will POST to that URL every time a subscribed event fires.
    """
    pass