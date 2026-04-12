"""SQLAlchemy ORM models for the URL shortener application."""

from sqlalchemy import Column, Integer, String
from app.core.database import Base


class URL(Base):
    """Represents a mapping from generated short code to a long URL.

    Attributes:
        id: Auto-incrementing primary key.
        long_url: The original URL to be shortened and redirect to.
        short_code: The generated short identifier (e.g., "X9D7FF").
    """

    __tablename__="urls"
    # primary key for the URL mapping
    id = Column(Integer, primary_key=True, index=True)

    # Target URL that the short code will redirect to.
    long_url = Column(String, nullable=False, unique=True)

    # Unique short code for quick lookup
    short_code = Column(String, unique=True, index=True)