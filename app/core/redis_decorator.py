import json
from functools import wraps
from app.models.url_model import URL

from app.models import url_model
from core.cache import get_cache, set_cache
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession


def cache_response(key_func, ttl=300):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            key = key_func(*args, **kwargs)
            cached = await get_cache(key)
            if cached:
                return json.loads(cached)
            result = await func(*args, **kwargs)
            encoded_result = jsonable_encoder(result)
            await set_cache(key, json.dumps(encoded_result), ttl)
            return wrapper
        return decorator
    

def url_cache_key(url: URL, db: AsyncSession):
    return f"url_shortcode:{url.short_code}"