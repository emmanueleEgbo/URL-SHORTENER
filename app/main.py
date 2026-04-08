from fastapi import FastAPI
from app.api.routes import router

app = FastAPI()

# Include the routes
app.include_router(router)

# Liveliness / health check endpoint
@app.get("/")
def root():
    return {"status": "ok", "message": "URL shortener is running"}