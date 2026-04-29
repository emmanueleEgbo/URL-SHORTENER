"""Entry point for the URL shortener application.

Run with:
    uvicorn app.main:app --reload
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api.v1.routes import v1_router
from app.api.v1.webhook_routes import webhook_router
from app.core.async_database import async_engine, Base
from app.core.cache_utilities import close_redis, init_redis
from app.models.url_model import URL
import logging


# Connect redis to our FastAPI app lifecycle so it can start and close properly authomatically
@asynccontextmanager
async def lifespan(app: FastAPI):
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    await init_redis()
    logging.info("REDIS INITIALIZED")

    yield
    
    await close_redis()

app = FastAPI(title="URL Shortener" ,lifespan=lifespan)


# Include the routes
app.include_router(v1_router)
app.include_router(webhook_router)

# Liveliness / health check endpoint
@app.get("/")
def root():
    return {"status": "ok", "message": "URL shortener is running"}