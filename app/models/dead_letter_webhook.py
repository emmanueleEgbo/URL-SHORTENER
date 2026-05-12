from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, JSON
from app.core.async_database import Base


class DeadLetterWebhook(Base):
    __tablename__="dead_letter_webhooks"

    id = Column(Integer, primary_key=True, autoincrement=True)
    webhook_id = Column(Integer, nullable=False, index=True)
    