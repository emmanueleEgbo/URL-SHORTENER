import os
from dotenv import load_dotenv
from redis.asyncio import Redis

# Load environment variables from .env
load_dotenv()

REDIS_HOST=os.getenv("REDIS_HOST")
REDIS_PORT=os.getenv("REDIS_PORT")
REDIS_DB=os.getenv("REDIS_DB")
REDIS_PASSWORD=os.getenv("REDIS_PASSWORD")

async def init_redis():
    """Initialize Redis connection on app startup."""
    global redis
    redis = Redis(
        host=REDIS_HOST,
        port=REDIS_PORT,
        db=REDIS_DB,
        password=REDIS_PASSWORD,
        decode_responses=True,
    )


async def close_redis():
    """Close Redis connection on app shutdown"""
    global redis
    if redis:
        await redis.close()
    

async def get_cache(key: str):
    if not redis:
        raise RuntimeError("Redis not initialized.")
    return await redis.get(key)


async def set_cache(key: str, value: str, ttl: int = 300):
    if not redis:
        raise RuntimeError("Redis not initialized.")
    await redis.set(key, value, ex=ttl)


async def delete_cache(key: str):
    if not redis:
        raise RuntimeError("Redis not initialized.")
    await redis.delete(key)