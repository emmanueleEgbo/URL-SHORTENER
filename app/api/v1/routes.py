"""FastAPI API routes for the URL shortener service.

All handlers are async. DB sessions are AsyncSession (asyncpg-backed).
Redis is checked first on the redirect hot path before hitting the DB.

Endpoints:
- POST   /v1/links               create a short link
- GET    /v1/links               list all stored links
- GET    /v1/links/{short_code}  redirect to original URL (307)
- DELETE /v1/links/{short_code}  delete a short link
"""

from fastapi import APIRouter, Depends, Header, HTTPException
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.async_database import get_db
from app.schemas.url_schema import URLCreate, URLResponse, PaginatedResponse
from app.services.url_service import (
    create_short_url_service, 
    get_long_url_service, 
    get_urls_service,
    delete_url_service,
)
from app.services import webhook_service
from fastapi.responses import RedirectResponse
from app.core.redis_decorator import cache_response, url_cache_key
from app.core.idempotency import get_idempotent_response, store_idempotent_response
from app.models.url_model import URL

v1_router = APIRouter(prefix="/v1", tags=["v1"])


@v1_router.get("/links", response_model=PaginatedResponse)
async def get_urls(db: AsyncSession = Depends(get_db)):
    """Create a short URL code for a provided long URL.

    Supports the Idempotency-Key header. Send the same UUID on retries and
    the original response is returned without creating a duplicate record.

    Args:
        p: Pydantic model containing the long_url to shorten.
        db: Async SQLAlchemy DB session dependency.
        idempotency_key: Optional client-generated UUID for safe retries.

    Returns:
        PaginatedResponse: A response object containing a list of URL instances,
        where each instance includes the `short_code` and `long_url`.
    """
    urls = await get_urls_service(db)

    return {
        "data": [URLResponse.model_validate(u) for u in urls],
    }


@v1_router.post("/links", response_model=URLResponse)
async def create_short_url(
    p: URLCreate, 
    db: AsyncSession = Depends(get_db),
    idempotency_key: Optional[str] = Header(None, alias="Idempotency-Key"),
) -> URLResponse:
    """Create a short URL code for a provided long URL.

    Args:
        p: Pydantic model containing the `long_url` to shorten.
        db: SQLAlchemy DB session dependency.

        Returns:
            URLResponse: The persisted URL record containing the `short_code` and `long_url`.
    """
    url = await create_short_url_service(db, str(p.long_url), p.title)
    
    # Hook webhook
    await webhook_service.fire_event(
        db,
        "url.created",
        {"short_code": url.short_code, "long_url": url.long_url, "title": url.title},
    )
    return url


@v1_router.get("/links/{short_code}")
@cache_response(url_cache_key, ttl=300)
async def redirect_to_long_url(short_code: str, db: AsyncSession = Depends(get_db)):
    """Redirect to the original long URL for the given short code.

    Args:
        short_code: The short code to resolve
        db: SQLAlchemy DB session dependency.

    Raises:
        HTTPException: 404 if the short code does not exist.

    Returns:
        RedirectResponse: A 307 redirect to the original `long_url`.
    """
    url = await get_long_url_service(db, short_code)
    # if not url:
    if url is None:
        raise HTTPException(status_code=404, detail="URL not found")
    
    await webhook_service.fire_event(
        db,
        "url.clicked",
        {"short_code": short_code, "long_url": url.long_url, "title": url.title},
    )
    
    # Use Starlette's RedirectResponse to send the client to the original URL.
    return RedirectResponse(url=url.long_url)


@v1_router.delete("/links/{short_code}", status_code=204)
async def delete_short_url(short_code: str, db: AsyncSession = Depends(get_db)):
    """Delete the URL mapping for the given short code.

    Also evicts the entry from Redis cache.

    Args:
        short_code: The short code to delete.
        db: Async SQLAlchemy DB session dependency.

    Raises:
        HTTPException: 404 if the short code does not exist.
    """
    deleted = await delete_url_service(db, short_code)
    if not deleted:
        raise HTTPException(status_code=404, detail="URL not found")
    await webhook_service.fire_event(db, "url.deleted", {"short_code": short_code})