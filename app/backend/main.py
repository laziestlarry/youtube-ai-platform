from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from .routers import video_creation, blueprints, users, auth
from .database import models, engine, database # Import the new database module

limiter = Limiter(key_func=get_remote_address)

# Create all database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Creator's Command Center API")

# --- CORS Middleware ---
# This is crucial for allowing the frontend to communicate with the backend
# when they are on different domains (as they will be in Cloud Run).
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict this to your frontend's URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Include API routers
app.include_router(video_creation.router, prefix="/api", tags=["Video Creation"])
app.include_router(blueprints.router, prefix="/api", tags=["Blueprints"])
app.include_router(users.router, prefix="/api", tags=["Users"])
app.include_router(auth.router, prefix="/api", tags=["Authentication"])

# Mount the 'frontend' directory to serve static assets like CSS and JS
app.mount("/static", StaticFiles(directory="app/frontend"), name="frontend_static")

# Mount the 'outputs' directory to serve user-generated files like animations
# This is crucial for the Brand Showcase feature to work.
app.mount("/media", StaticFiles(directory="outputs"), name="media_files")

@app.get("/", include_in_schema=False)
async def read_index():
    # Serve the main dashboard page
    return FileResponse("app/frontend/dashboard_concept.html")

@app.get("/login", include_in_schema=False)
async def read_login():
    return FileResponse("app/frontend/login.html")

@app.get("/forgot-password", include_in_schema=False)
async def read_forgot_password():
    return FileResponse("app/frontend/forgot-password.html")

@app.get("/reset-password", include_in_schema=False)
async def read_reset_password():
    return FileResponse("app/frontend/reset-password.html")