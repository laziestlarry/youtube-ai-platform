from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.backend.api.v1.api import api_router
from app.backend.core.config import settings


app = FastAPI(title="YouTube AI Platform")

app.include_router(api_router, prefix=settings.API_V1_STR)

# This should be the last route registration
app.mount("/", StaticFiles(directory="frontend/dist", html=True), name="static")

@app.get("/api/health", tags=["Health"])
def health_check():
    return {"status": "ok"}