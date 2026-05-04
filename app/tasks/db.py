"""Synchronous SQLAlchemy session for use inside Celery tasks.

Celery workers are not async — they run in a plain thread, so they need a
regular (sync) engine and session, not the async ones used by FastAPI.
"""