"""Periodic Celery tasks for analytics and housekeeping.

Both tasks are registered in the beat_schedule inside celery_app.py:
  - daily_analytics_rollup  → midnight UTC every day
  - cleanup_expired_links   → every hour on the hour
"""