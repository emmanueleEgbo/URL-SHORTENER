"""Database setup and session management for URL shortener app.

This module configures the SQLAlchemy engine, session factory, and provides the 
`get_db` dependency used in FastAPI routes to inject a scoped database session.

Environment:
    - Expects `DATABASE_URL` to be defined in the environment (read from `.env`).

Notes: 
    - The engine and session here are synchronous. If you plan to migrate to asyn
    endpoints, use `sqlalchemy.ext.asyncio` and an async session pattern.
"""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.ext.asyncio import create_async_engine # for future use
from dotenv import load_dotenv

# Load environment variable from a `.env` file
load_dotenv()

# Connection string for the database
DATABASE_URL = os.getenv("DATABASE_URL")

# Create a synchronous SQLAlchemy engine bound to the connection string
engine = create_engine(DATABASE_URL)

# Configure a session factory. `autocommit` and `autoflush` are disabled for explicit control.
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

# Base class for SQLAlchemy models to inherit from.
Base = declarative_base()