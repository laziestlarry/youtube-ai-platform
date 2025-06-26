import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str

    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8

    GEMINI_API_KEY: str  # Added for direct Gemini access if needed
    SERPER_API_KEY: str | None = None  # Added for consistency with mini_app
    # For production, this should be a Cloud SQL connection string, e.g.,
    # "postgresql+asyncpg://user:pass@host:port/db"
    # For local dev, it can remain "sqlite+aiosqlite:///./youtube_ai.db"
    DATABASE_URL: str

    # Google Cloud Settings
    GCP_PROJECT_ID: str | None = None
    GCP_REGION: str | None = "us-central1"
    GCS_BUCKET_NAME: str | None = None  # Bucket for storing generated media

    # Cloud Tasks / Worker configuration
    WORKER_URL: str | None = None  # URL of the private worker Cloud Run service
    TASK_QUEUE_NAME: str | None = None  # Name of the Cloud Tasks queue
    TASK_QUEUE_LOCATION: str | None = None  # Location of the Cloud Tasks queue
    WORKER_SA_EMAIL: str | None = None  # Email of the worker's service account

    class Config:
        case_sensitive = True
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
