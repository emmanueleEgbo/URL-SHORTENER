from datetime import datetime
from enum import Enum
from typing import List
from pydantic import BaseModel


class WebhookEvent(str, Enum):
    URL_CREATED = "url.created"
    URL_CLICKED = "url.clicked"
    URL_DELETED = "url.deleted"


class WebhookCreate(BaseModel):
    name: str
    url: str
    event: List[WebhookEvent]