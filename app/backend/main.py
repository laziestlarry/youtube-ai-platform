import os
from pathlib import Path

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


# --- Static Files Mounting ---
# This section makes the app robust for both local development and Docker.

# Define the project root directory. This assumes main.py is in app/backend/
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

# Define potential base directories for the frontend build output
docker_build_path = PROJECT_ROOT / "app" / "static"
local_build_path = PROJECT_ROOT / "frontend" / "dev_dashboard" / "build"

build_dir = None
if docker_build_path.is_dir():
    build_dir = docker_build_path
elif local_build_path.is_dir():
    build_dir = local_build_path

if build_dir:
    # The static assets (JS, CSS) are in a 'static' subdirectory within the build output.
    # We mount this subdirectory to the '/static' URL path.
    app.mount(
        "/static",
        StaticFiles(directory=build_dir / "static"),
        name="static_assets"
    )

    @app.get("/{full_path:path}", include_in_schema=False)
    async def serve_react_app(full_path: str):
        index_path = build_dir / "index.html"
        if index_path.exists():
            return FileResponse(index_path)
        return FileResponse("index.html not found", status_code=404)
else:
    print("WARNING: Static file directory not found. Frontend will not be served.")
    print(f"         Checked for '{docker_build_path}' and '{local_build_path}'.")
    print("         Please run 'yarn build' in 'frontend/dev_dashboard'.")
