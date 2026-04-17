import os
from redis.asyncio import Redis
from app.core.config import settings
import logging

redis = None

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

        await redis.ping() # verify connection
        logging.info("REDIS CONNECTED")
    except Exception:
        logging.info("Redis not available")
        redis = None


async def close_redis():
    """Close Redis connection on app shutdown"""
    global redis
    if redis:
        await redis.close()
    

async def get_cache(key: str):
    """Retrieve a value from Redis cache by key.

    Performs an asynchronous lookup in Redis for the given key. If Redis
    is not initialized, raises an error to prevent silent failures.

    Args:
        key: The cache key to retrieve the value for.

    Returns:
        The cached value associated with the key, or None if the key
        does not exist in the cache.

    Raises:
        RuntimeError: If the Redis client has not been initialized.
    """
    if redis is None:
        return None
    return await redis.get(key)


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
        None.

    Raises:
        RuntimeError: If the Redis client has not been initialized.
    """
    if redis is None:
        return
    await redis.set(key, value, ex=ttl)


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
    if redis is None:
        return
    await redis.delete(key)