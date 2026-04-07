"""Database setup and session management for URL shortener app.

This module configures the SQLAlchemy engine, session factory, and provides the 
`get_db` dependency used in FastAPI routes to inject a scoped database session.

Environment:
    - Expects `DATABASE_URL` to be defined in the environment (read from `.env`).

Notes: 
    - The engine and session here are synchronous. If you plan to migrate to asyn
    endpoints, use `sqlalchemy.ext.asyncio` and an async session pattern.
"""