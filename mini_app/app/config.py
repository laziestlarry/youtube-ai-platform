from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Optional

class MiniAppConfig(BaseSettings):
    app_port: int = Field(default=8080, env="APP_PORT")
    main_platform_url: str = Field(default="http://localhost:8000", env="MAIN_PLATFORM_URL")
    # OpenAI key is no longer the primary, but we can keep it for comparison or fallback
    openai_api_key: Optional[str] = Field(None, env="OPENAI_API_KEY")
    serper_api_key: Optional[str] = Field(None, env="SERPER_API_KEY")
    gcp_project_id: str = Field(..., env="GCP_PROJECT_ID")
    gcp_region: str = Field("us-central1", env="GCP_REGION")

    class Config:
        env_file_encoding = 'utf-8'

settings = MiniAppConfig()