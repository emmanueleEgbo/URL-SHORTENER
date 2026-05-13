from datetime import datetime
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel


class WebhookEvent(str, Enum):
    URL_CREATED = "url.created"
    URL_CLICKED = "url.clicked"
    URL_DELETED = "url.deleted"


class WebhookCreate(BaseModel):
    name: str
    url: str
    events: List[WebhookEvent]


class WebhookResponse(BaseModel):
    """Response model representing a registered webhook configuration.

    Attributes:
        id: Unique identifier of the webhook.
        name: Human-readable name assigned to the webhook.
        url: The endpoint URL where events will be delivered.
        events: List of event types that trigger this webhook.
        is_active: Indicates whether the webhook is currently enabled.
        created_at: Timestamp indicating when the webhook was created.
    """
    id: int
    name: str
    url: str
    events: List[str]
    is_active: bool
    created_at: datetime

    class Config:
        # Allow creating this schema directly from ORM objects (e.g., SQLAlchemy models)
        from_attributes=True


class DLQEntryResponse(BaseModel):
    id: int
    webhook_id: int
    webhook_url: str
    payload: dict
    failure_reason: Optional[str] = None
    attempt_count: int
    failed_at: datetime