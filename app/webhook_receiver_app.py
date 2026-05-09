"""A local webhook receiver app to use for testing webhook in place of webhook.site"""

from fastapi import FastAPI, Request


app = FastAPI()

@app.post("/webhook")
async def receive_webhook(request: Request):
    """
    Receive incoming webhook events.

    This endpoint is used as a webhook receiver for external services or
    internal background jobs (e.g., Celery tasks). It accepts a JSON payload,
    logs the received data, and returns a simple acknowledgment response.

    Args:
        request (Request): The incoming HTTP request containing a JSON body.

    Returns:
        dict: A simple confirmation response indicating successful receipt.
              Example: {"ok": True}

    Notes:
        - The payload is expected to be valid JSON.
        - This endpoint is typically used for testing or local development.
        - In production, consider adding authentication (e.g., HMAC signature verification)
          to ensure the webhook is coming from a trusted source.
    """
    data = await request.json()
    print("WEBHOOK RECEIVED:")
    print(data)
    return {"ok": True}