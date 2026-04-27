"""Webhook delivery and CRUD service.

How it works end-to-end:
  1. A caller registers a webhook via create_webhook() — stores the target URL +
     the list of events it cares about.
  2. When something interesting happens (URL created, clicked, deleted) the route
     handler calls fire_event().
  3. fire_event() loads all active webhooks whose `events` list includes the
     current event, builds a JSON payload, and schedules an async HTTP POST to
     each target URL using asyncio.create_task() — so the delivery is completely
     non-blocking; the API response returns immediately.
"""