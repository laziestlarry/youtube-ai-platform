import argparse
import uuid
from app.backend.core.config import settings
from app.backend.models.video import Video
from app.services.gcs_utils import \
    upload_to_gcs  # Assumes a new utility for GCS
from app.services.script_generator_gemini import generate_script_with_gemini
from app.services.tts_google import synthesize_speech_google


def run_video_production_pipeline(video: Video, advanced=False):
    """
    Executes the full video production pipeline for a given video record.
    This to be triggered by a background worker (e.g., Celery, Cloud Tasks).
    """
    print(
        f"[Pipeline] Starting for Video ID: {video.id}, Title: {video.title}")

    # 1. Generate Script using Vertex AI
    script = generate_script_with_gemini(video.title, video.description)
    print(f"[Pipeline] Generated script for Video ID {video.id}")

    # 2. Synthesize Speech using Google Cloud TTS
    # This should return the audio content in-memory
    audio_content = synthesize_speech_google(script)
    audio_blob_name = f"videos/{video.id}/generated_audio.mp3"

    # 3. Upload audio to Google Cloud Storage
    audio_gcs_uri = upload_to_gcs(
        audio_content, settings.GCS_BUCKET_NAME, audio_blob_name
    )
    print(f"[Pipeline] Synthesized audio and uploaded to: {audio_gcs_uri}")

    # ... Subsequent steps would follow ...

    print(f"[Pipeline] Pipeline complete for Video ID: {video.id}.")


def main():
    """
    Main entry point for the script. Parses command-line arguments
    and triggers the video production pipeline.
    """
    parser = argparse.ArgumentParser(description="Run the full video generation pipeline.")
    parser.add_argument("--topic", type=str, required=True, help="The topic or title for the new video.")
    parser.add_argument("--description", type=str, default="", help="An optional description for the video.")
    args = parser.parse_args()

    # Create a mock Video object to drive the pipeline
    video_data = Video(id=str(uuid.uuid4()), title=args.topic, description=args.description)

    run_video_production_pipeline(video_data)

if __name__ == "__main__":
    main()
