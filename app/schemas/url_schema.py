"""Pydantic schemas for request/response validation in the URL shortener.

These models define the shape of the data accepted by and returned from the API endpoints.
They provide runtime validation and automatic documentation for FastAPI.
"""

from typing import List
from pydantic import BaseModel, HttpUrl

class URLCreate(BaseModel):
    """Payload for creating a short URL.

    Attributes:
        long_url: The original URL to shorten
    """
    long_url: HttpUrl


class URLResponse(BaseModel):
    """Response model representing a stored URL mapping.

    Attributes:
        short_code: The generated short code identifier (e.g., "X9D7EE")
        long_url: The original URL to which clients will be redirected.
    """

    short_code: str
    long_url: HttpUrl

    class Config:
        # Allow creating this scheme directly from ORM objects (e.g., SQLAlchemy models)
        from_attributes=True

class PaginatedResponse(BaseModel):
    data: List[URLResponse]