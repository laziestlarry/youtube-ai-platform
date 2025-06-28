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

    # DIAGNOSTIC STEP: Since multiple Gemini models (1.5-pro, 1.0-pro, gemini-pro)
    # have returned a 404 Not Found error, we are switching to a different,
    # widely available PaLM 2 model ('text-bison@002') to test if the project
    # has access to any generative models in Vertex AI.
    # If this succeeds, it points to a project-specific issue with Gemini access.
    model_name = "text-bison@002"
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