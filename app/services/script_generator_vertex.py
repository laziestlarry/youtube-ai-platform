import vertexai
from vertexai.generative_models import GenerativeModel

from app.backend.core.config import settings


def generate_script_with_gemini(title: str, description: str) -> str:
    """
    Generates a video script using Google's Gemini model via Vertex AI.

    Args:
        title: The title of the video.
        description: A brief description of the video's content.

    Returns:
        The generated script as a string.
    """
    print("Initializing Vertex AI...")
    # The project and location are often discovered from the environment,
    # but explicit initialization is more robust in a containerized environment.
    vertexai.init(project=settings.GCP_PROJECT_ID, location=settings.GCP_REGION)

    # Use a stable, generally available model version.
    # The specific version 'gemini-1.0-pro-002' was not found.
    # We will use the most common stable identifier, 'gemini-pro', which is an alias
    # for the latest stable 1.0 Pro model.
    model_name = "gemini-pro"
    print(f"Using Vertex AI model: {model_name}")
    model = GenerativeModel(model_name)

    prompt = f"""
    Create a compelling and engaging YouTube video script based on the following topic.
    The script should be well-structured, with a clear introduction, main body, and conclusion.
    It should be suitable for a text-to-speech engine.

    Video Title: {title}
    Video Description: {description}

    Please provide only the script content, without any additional commentary or formatting.
    """

    print(f"Generating script for title: '{title}'...")
    # Adding explicit generation and safety settings for robustness
    response = model.generate_content(
        prompt,
        generation_config={
            "temperature": 0.7,
            "top_p": 1.0,
            "max_output_tokens": 2048,
        },
    )
    print("Script generation successful.")

    return response.text