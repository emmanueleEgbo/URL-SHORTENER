import os
from dotenv import load_dotenv
from redis.asyncio import Redis

# Load environment variables from .env
load_dotenv()

async def init_redis():
    """Initialize Redis connection on app startup."""
    global redis
    redis = Redis(
        host=os.get
    )