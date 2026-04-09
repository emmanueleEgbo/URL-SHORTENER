import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from dotenv import load_dotenv

# Load environment variable from a `.env` file
load_dotenv()

# Connection string for the async database
DATABASE_URL = os.getenv("DATABASE_URL")

async_engine = create_async_engine(DATABASE_URL, echo=True)

# Async session factory
AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

base = declarative_base()

# FastAPI dependency
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session