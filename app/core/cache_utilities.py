import os
import logging
from redis.asyncio import Redis
from app.core.config import settings
from typing import Optional

logger = logging.getLogger(__name__)

redis: Optional[Redis] = None

async def init_redis():
    """Initialize Redis connection on app startup."""
    global redis

    try:
        redis = Redis(
        host=settings.redis_host,
        port=settings.redis_port,
        db=settings.redis_db,
        password=settings.redis_password,
        decode_responses=True,
        )
        logger.info("Redis connection initialized")

    except Exception:
        logger.info("Redis not available")
        redis = None


async def close_redis():
    """Close Redis connection on app shutdown"""
    global redis
    if redis:
        await redis.close()
        redis = None
    logger.info("Redis connection closed")


async def _get_redis() -> Redis:
    if redis is None:
        raise RuntimeError("Redis not initialized")
    return redis
    

async def get_cache(key: str):
    """Retrieve a value from Redis cache by key.

    Args:
        key: The cache key to retrieve the value for.

    Returns:
        The cached value associated with the key, or None if the key
        does not exist in the cache.
    
    Raises:
        Runtime error stating that redis is not initialized.
    """
    r = await _get_redis()
    return await r.get(key)


async def set_cache(key: str, value: str, ttl: int = 300):
    """Store a value in Redis cache with an optional expiration time.

    Performs an asynchronous write to Redis, associating the given key
    with the provided value. A time-to-live (TTL) can be set to ensure
    the cached data expires automatically.

    Args:
        key: The cache key under which the value will be stored.
        value: The value to store in the cache.
        ttl: Time-to-live in seconds before the key expires (default: 300).

    Returns:
        None
    """
    r = await _get_redis()
    await r.set(key, value, ex=ttl)


async def delete_cache(key: str):
    """Delete a value from Redis cache by key.

    Performs an asynchronous deletion of the specified key from Redis.
    If the key does not exist, the operation completes silently.

    Args:
        key: The cache key to delete.

    Returns:
        None.

    Raises:
        RuntimeError: If the Redis client has not been initialized.
    """
    r = await _get_redis()
    await r.delete(key)

