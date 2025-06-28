import google.generativeai as genai
import os

from app.backend.core.config import settings


def generate_script_with_gemini(title: str, description: str) -> str:
    """
    Generates a video script using Google's Gemini model via Vertex AI.

    This version uses the google-generativeai library with a direct API key
    as a diagnostic step to bypass potential project/region availability issues
    with the Vertex AI SDK.

    Args:
        title: The title of the video.
        description: A brief description of the video's content.

    Returns:
        The generated script as a string.
    """
    print("Initializing Google Generative AI client with API Key...")
    genai.configure(api_key=os.environ["GEMINI_API_KEY"])
    # The API returned a 404 Not Found for 'gemini-1.0-pro'. This indicates
    # that for the API key's endpoint, a more specific model name is required.
    # We will use 'gemini-1.5-pro-latest', which is the recommended stable model.
    model = genai.GenerativeModel("gemini-1.5-pro-latest")

    prompt = f"""
    Create a compelling and engaging YouTube video script based on the following topic.
    The script should be well-structured, with a clear introduction, main body, and conclusion.
    It should be suitable for a text-to-speech engine.

    Video Title: {title}
    Video Description: {description}

    Please provide only the script content, without any additional commentary or formatting.
    """

    print(f"Generating script for title: '{title}'...")
    response = model.generate_content(prompt)
    print("Script generation successful.")

    return response.text