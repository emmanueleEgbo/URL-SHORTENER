import json
from functools import wraps
from app.models.url_model import URL

from app.models import url_model
from app.core.cache_utilities import get_cache, set_cache
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

            return result
        
        return wrapper
    return decorator
    

def url_cache_key(short_code: str, **kwargs):
    return f"url_shortcode:{short_code}"