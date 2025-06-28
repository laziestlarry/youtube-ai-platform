import argparse
import uuid
from app.backend.core.config import settings
from app.backend.models.video import Video
from google.api_core.exceptions import Forbidden, NotFound
from app.services.gcs_utils import \
    upload_to_gcs  # Assumes a new utility for GCS
from app.services.script_generator_gemini import generate_script_with_gemini
from app.services.tts_google import synthesize_speech_google
from app.services.video_generator import generate_video_from_assets


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
    try:
        audio_gcs_uri = upload_to_gcs(
            audio_content, settings.GCS_BUCKET_NAME, audio_blob_name
        )
        print(f"[Pipeline] Synthesized audio and uploaded to: {audio_gcs_uri}")
    except NotFound:
        print(
            f"ERROR: Google Cloud Storage bucket '{settings.GCS_BUCKET_NAME}' not found."
        )
        print(
            "Please create the bucket in your Google Cloud project or correct the GCS_BUCKET_NAME in your settings."
        )
        raise
    except Forbidden as e:
        print(f"ERROR: Permission denied when trying to access Google Cloud Storage bucket '{settings.GCS_BUCKET_NAME}'.")
        print("This could be due to missing IAM permissions for the service account or a project billing issue.")
        print(f"Detailed error from Google Cloud: {e.message}")
        raise

    # 4. Generate Video from script and audio
    print(f"[Pipeline] Generating video for Video ID: {video.id}...")
    # This function will take the script and audio URI and produce a video file
    final_video_content = generate_video_from_assets(script, audio_gcs_uri)
    print(f"[Pipeline] Video generation successful for Video ID: {video.id}")

    # 5. Upload final video to GCS
    # Note: The 'upload_to_gcs' utility may need to be updated to handle
    # the 'video/mp4' content type if it's currently hardcoded for audio.
    video_blob_name = f"videos/{video.id}/final_video.mp4"
    video_gcs_uri = upload_to_gcs(
        final_video_content, settings.GCS_BUCKET_NAME, video_blob_name
    )
    print(f"[Pipeline] Final video uploaded to: {video_gcs_uri}")

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
