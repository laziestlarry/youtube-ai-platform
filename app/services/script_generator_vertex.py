import vertexai
from vertexai.generative_models import GenerativeModel

from app.backend.core.config import settings


def generate_script_with_gemini(title: str, description: str) -> str:
    """
    Generates a YouTube video script using Google's Gemini model.
    """
    vertexai.init(project=settings.GCP_PROJECT_ID, location=settings.GCP_REGION)
    model = GenerativeModel("gemini-1.5-pro-preview-0409")

    prompt = f"""
    You are a professional YouTube scriptwriter.
    Write a compelling and engaging video script based on the following details:
    Video Title: {title}
    Video Description: {description}

    The script should have a hook, main content, and a call to action. Structure it clearly.
    """
    response = model.generate_content(prompt)
    return response.text
