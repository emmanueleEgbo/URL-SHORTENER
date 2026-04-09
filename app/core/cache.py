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
        host=os.get
    )