import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    # Environment mode: 'production' or 'test'. Defaulting to 'test' for low-cost setup.
    ENV: str = "test"

    # Database
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/appdb"

    # Redis
    REDIS_URL: str = "redis://redis:6379/0"

    # JWT Authentication
    SECRET_KEY: str = "a_very_secret_key_for_local_dev"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Google OAuth
    GOOGLE_CLIENT_ID: str = ""
    GOOGLE_CLIENT_SECRET: str = ""
    GOOGLE_REDIRECT_URI: str = "http://localhost:8000/login"

    class Config:
        env_file = ".env"

# Create a single, importable instance of the settings
settings = Settings()

# Override settings for the test environment
if settings.ENV == "test":
    # Use a file-based SQLite database on the container's ephemeral filesystem.
    # This is the absolute lowest cost, but data will be lost on container restart.
    db_path = "/usr/src/app/outputs/test.db"
    settings.DATABASE_URL = f"sqlite:///{db_path}"
    # Use the redis server running in the same container
    settings.REDIS_URL = "redis://localhost:6379/0"