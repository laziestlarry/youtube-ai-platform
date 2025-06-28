import time
import requests
from abc import ABC, abstractmethod

class BaseVideoProvider(ABC):
    """Abstract base class for a video generation provider."""
    def __init__(self, api_key: str):
        if not api_key:
            raise ValueError("API key is required for video generation provider.")
        self.api_key = api_key

    @abstractmethod
    def generate(self, script: str, audio_url: str) -> bytes:
        """The main method to generate a video."""
        pass

class FlikiProvider(BaseVideoProvider):
    """A mock client for the Fliki video generation service."""
    def generate(self, script: str, audio_url: str) -> bytes:
        print("[Video Provider: Fliki] Initializing video creation with user's API key.")
        print("[Video Provider: Fliki] Simulating job with stock footage, animations, and LUTs.")
        # In a real implementation, you would make an API call to Fliki here
        # using self.api_key in the authorization header.
        time.sleep(15) # Simulate premium rendering time
        video_url = "http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerJoyrides.mp4"
        print(f"[Video Provider: Fliki] Downloading final video from: {video_url}")
        response = requests.get(video_url, timeout=60)
        response.raise_for_status()
        return response.content

class PictoryProvider(BaseVideoProvider):
    """A mock client for the Pictory video generation service."""
    def generate(self, script: str, audio_url: str) -> bytes:
        print("[Video Provider: Pictory] Initializing video creation with user's API key.")
        print("[Video Provider: Pictory] Simulating job with AI-selected visuals.")
        time.sleep(12) # Simulate rendering time
        video_url = "http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerFun.mp4"
        print(f"[Video Provider: Pictory] Downloading final video from: {video_url}")
        response = requests.get(video_url, timeout=60)
        response.raise_for_status()
        return response.content

def get_provider(provider_name: str, api_key: str) -> BaseVideoProvider:
    """Factory function to get a video provider instance."""
    providers = {
        "fliki": FlikiProvider,
        "pictory": PictoryProvider,
    }
    provider_class = providers.get(provider_name.lower())
    if not provider_class:
        raise ValueError(f"Unsupported video provider: {provider_name}")
    return provider_class(api_key=api_key)

def generate_video_from_assets(script: str, audio_gcs_uri: str, provider_name: str, api_key: str) -> bytes:
    """
    Generates a video by selecting a provider and using a user-provided API key.

    Args:
        script: The text script for the video.
        audio_gcs_uri: The GCS URI of the generated audio file.
        provider_name: The name of the video generation service (e.g., 'fliki').
        api_key: The user's API key for that service.

    Returns:
        The raw byte content of the generated MP4 video.
    """
    try:
        # Get the appropriate provider client
        provider = get_provider(provider_name, api_key)
        # Convert gs:// URI to a public URL for the API
        public_audio_url = audio_gcs_uri.replace("gs://", "https://storage.googleapis.com/")
        # Generate the video
        video_content = provider.generate(script, public_audio_url)
        return video_content
    except (ValueError, requests.exceptions.RequestException) as e:
        print(f"ERROR in video generation: {e}")
        raise