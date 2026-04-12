"""FastAPI API for the URL shortener service.

Exposes three endpoints:
-  POST /shorten: accepts a long URL and returns a generated short code with the original URL.
-  GET /{short_code}: Redirects the clients to the original long URL if the short code exists.
-  GET /urls: Retrieves a list of stored URL model instances, each including the short_code and long_url.
"""

from fastapi import APIRouter, Depends, HTTPException
from typing import List
#from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
#from app.core.database import get_db
from app.core.async_database import get_db
from app.schemas.url_schema import URLCreate, URLResponse, PaginatedResponse
from app.services.url_service import create_short_url_service, get_long_url_service, get_urls_service
from fastapi.responses import RedirectResponse
from app.core.redis_decorator import cache_response, url_cache_key
from app.models.url_model import URL

router = APIRouter(prefix="/v1")

@router.get("/urls", response_model=PaginatedResponse)
async def get_urls(db: AsyncSession = Depends(get_db)):
    """Retrieve all stored URLs.

    Args:
        db: SQLAlchemy asynchronous database session dependency.

    Returns:
        PaginatedResponse: A response object containing a list of URL instances,
        where each instance includes the `short_code` and `long_url`.
    """
    urls = await get_urls_service(db)

    return {
        "data": [URLResponse.model_validate(u) for u in urls],
    }


@router.post("/shorten", response_model=URLResponse)
async def create_short_url(p: URLCreate, db: AsyncSession = Depends(get_db)) -> URLResponse:
    """Create a short URL code for a provided long URL.

    Args:
        p: Pydantic model containing the `long_url` to shorten.
        db: SQLAlchemy DB session dependency.

        Returns:
            URLResponse: The persisted URL record containing the `short_code` and `long_url`.
    """
    url = await create_short_url_service(db, p.long_url)
    return url


@router.get("/{short_code}")
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
    if not url:
        raise HTTPException(status_code=404, detail="URL not found")
    
    # Use Starlette's RedirectResponse to send the client to the original URL.
    return RedirectResponse(url=url.long_url)