from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from .routers import commander_api
from starlette.responses import FileResponse
from .config import settings
import uvicorn
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="YouTube Income Commander Mini",
    description="MVP for rapid commercial outcome YouTube idea generation and main platform initiation.",
    version="0.1.0"
)

# API routes should be declared before the static file mounting.
app.include_router(commander_api.router, prefix="/api/mini")

@app.get("/health")
async def health():
    return {"status": "ok"}

# Mount the 'static' directory where the React build output is stored.
# The path "mini_app/static" is relative to the Docker WORKDIR /app.
app.mount("/static", StaticFiles(directory="mini_app/static"), name="static")

# Catch-all route to serve the React app's index.html for any non-API, non-file path.
# This is crucial for client-side routing to work.
@app.get("/{full_path:path}")
async def serve_react_app(full_path: str):
    return FileResponse("mini_app/static/index.html")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=settings.app_port)