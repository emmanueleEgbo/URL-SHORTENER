from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.async_database import get_db
from app.schemas.webhooks_schema import WebhookCreate, WebhookResponse
from app.services import webhook_service


webhook_router = APIRouter(prefix="/v1/webhooks", tags=["webhooks"])