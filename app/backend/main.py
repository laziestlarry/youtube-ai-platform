from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse

from app.backend.api.v1.api import api_router
from app.backend.core.config import settings

app = FastAPI(title="YouTube AI Platform")

# API routes must be included before the frontend routes.
app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/api/health", tags=["Health"])
def health_check():
    return {"status": "ok"}

# Mount the 'static' directory where the React build output is stored.
# The path "app/static" is relative to the Docker WORKDIR /app.
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Catch-all route to serve the React app's index.html for any non-API, non-file path.
# This is crucial for client-side routing to work correctly.
@app.get("/{full_path:path}", include_in_schema=False)
async def serve_react_app(full_path: str):
    return FileResponse("app/static/index.html")
