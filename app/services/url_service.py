"""Business logic for creating and resolving shortened URLs.

This module contains small service helpers used by the API layer. 
It is kept framework-agnostic and operates on SQLAlchemy sessions
and models only.
"""

import random
import string
from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.url_model import URL

def generate_short_code(length: int = 6) -> str:
    """Generate psudo-random alphanumeric short code.

    Uses upper/lowercase letters and digits. Collisons are possible but
    unlikely for small datasets. For production, consider enforcing uniqueness by checking the database or using a more robust strategy.

    Args:
        length: Number of characters in the generated code (default: 6)

    Returns:
        A random alphanumeric string of the requested length.
    """
    return "".join(random.choices(string.ascii_letters + string.digits, k=length))


async def create_short_url_service(db: AsyncSession, long_url: str) -> URL:
    """Create or return an existing short URL mapping.

    Note:
        This implementation does not currently check for collisions. For a
        production system, add a retry loop to regenerate the code when a
        uniqueness constraint violation occurs.

    Args:
        db: Active SQLAlchemy session.
        long_url: The original URL to be shorten

    Returns:
        The persisted `URL` model instance.
    """

    # Check if long_url already exists and return it
    result = await db.execute(select(URL).where(URL.long_url == long_url))
    existing_long_url = result.scalar_one_or_none()

    if existing_long_url:
        return existing_long_url # Return existing mapping immediately


    # Check if shortcode already exists in DB and prevent collision.
    max_attempts = 10
    attempts = 0
    short_code = ""

    while attempts < max_attempts:
        short_code = generate_short_code()

        result = await db.execute(
            select(URL).where(URL.short_code == short_code)
        )
        existing = result.scalar_one_or_none()

        if not existing:
            break

        attempts += 1
    
    else:
        raise Exception("Failed to generate unique short code.")

    new_url = URL(long_url=long_url, short_code=short_code)
    
    db.add(new_url)
    await db.commit()
    await db.refresh(new_url)

    return new_url


async def get_long_url_service(db: AsyncSession, short_code: str) -> Optional[URL]:
    """Retrieve the stored URL mapping by its short code.

    Args:
        db: Active SQLAlchemy session.
        short_code: The short code to look up.

    Returns:
        The `URL` instance if found, otherwise `None`.
    """
    result = await db.execute(
        select(URL).where(URL.short_code == short_code)
    )
    # return db.query(URL).filter(URL.short_code==short_code).first()
    return result.scalar_one_or_none()


async def get_urls_service(db: AsyncSession):
    """Retrieve all URL records from the database.

    Executes an asynchronous query to fetch all entries from the URL table.
    Returns a list of ORM model instances. For large datasets, consider
    adding pagination to avoid performance issues.

    Args:
        db: Async SQLAlchemy session used to interact with the database.

    Returns:
        A list of URL model instances representing all stored URLs.
    """
    result = await db.execute(select(URL))
    return result.scalars().all()