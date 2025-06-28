import argparse
import uuid
import time
from dataclasses import dataclass
from app.backend.core.config import settings
from app.backend.models.video import Video
from google.api_core.exceptions import Forbidden, NotFound
from app.services.gcs_utils import \
    upload_to_gcs  # Assumes a new utility for GCS
from app.services.script_generator_gemini import generate_script_with_gemini
from app.services.audio_enhancer import mix_audio_with_music
from app.services.tts_google import synthesize_speech_google
from app.services.video_generator import generate_video_from_assets

@dataclass
class UserConfig:
    """A simple data class to hold user-specific configurations."""
    video_provider: str
    provider_api_key: str
    add_background_music: bool = False

def _generate_script(video: Video) -> str:
    """Step 1: Generate script using Vertex AI."""
    print(f"[Pipeline] Generating script for title: '{video.title}'...")
    script = generate_script_with_gemini(video.title, video.description)
    print(f"[Pipeline] Script generation successful for Video ID {video.id}")
    return script

def _synthesize_and_upload_audio(video_id: str, script: str, user_config: UserConfig) -> str:
    """Step 2 & 3: Synthesize speech, optionally add music, and upload to GCS."""
    print("[Pipeline] Synthesizing speech...")
    audio_content = synthesize_speech_google(script)
    print("[Pipeline] Speech synthesis successful.")

    if user_config.add_background_music:
        print("[Pipeline] Enhancing audio with background music...")
        # A real implementation would extract keywords from the script to pass here
        audio_content = mix_audio_with_music(audio_content, keywords=["inspirational"])

    audio_blob_name = f"videos/{video_id}/generated_audio.mp3"
    print(f"[Pipeline] Uploading audio to gs://{settings.GCS_BUCKET_NAME}/{audio_blob_name}...")
    try:
        audio_gcs_uri = upload_to_gcs(
            audio_content, settings.GCS_BUCKET_NAME, audio_blob_name
        )
        print(f"[Pipeline] Audio uploaded to: {audio_gcs_uri}")
        return audio_gcs_uri
    except NotFound:
        print(f"ERROR: GCS bucket '{settings.GCS_BUCKET_NAME}' not found.")
        raise
    except Forbidden as e:
        print(f"ERROR: Permission denied for GCS bucket '{settings.GCS_BUCKET_NAME}'.")
        print("Check service account permissions and project billing status.")
        print(f"Detailed error: {e.message}")
        raise

def _generate_and_upload_video(
    video_id: str, script: str, audio_gcs_uri: str, user_config: UserConfig
) -> str:
    """Step 4 & 5: Generate video and upload to GCS."""
    print(f"[Pipeline] Generating video for Video ID: {video_id}...")
    final_video_content = generate_video_from_assets(
        script, audio_gcs_uri, user_config.video_provider, user_config.provider_api_key
    )
    print(f"[Pipeline] Video generation successful for Video ID: {video_id}")

    video_blob_name = f"videos/{video_id}/final_video.mp4"
    print(f"[Pipeline] Uploading final video to gs://{settings.GCS_BUCKET_NAME}/{video_blob_name}...")
    # The 'upload_to_gcs' utility needs to handle 'video/mp4' content type.
    # We assume it does or can be modified to do so.
    video_gcs_uri = upload_to_gcs(
        final_video_content, settings.GCS_BUCKET_NAME, video_blob_name
    )
    print(f"[Pipeline] Final video uploaded to: {video_gcs_uri}")
    return video_gcs_uri

def run_video_production_pipeline(video: Video, user_config: UserConfig):
    """
    Executes the full video production pipeline for a given video record.
    This is triggered by a background worker (e.g., Cloud Tasks).
    """
    start_time = time.time()
    print(
        f"[Pipeline] Starting for Video ID: {video.id}, Title: {video.title}")

    try:
        # Step 1: Generate Script
        script = _generate_script(video)

        # Steps 2 & 3: Synthesize and Upload Audio
        audio_gcs_uri = _synthesize_and_upload_audio(video.id, script, user_config)

        # Steps 4 & 5: Generate and Upload Video
        video_gcs_uri = _generate_and_upload_video(
            video.id, script, audio_gcs_uri, user_config
        )

        # Future Step: Update database with final video URI
        # print(f"[Pipeline] Updating database for video {video.id} with URI: {video_gcs_uri}")

        total_time = time.time() - start_time
        print(f"[Pipeline] Successfully completed for Video ID: {video.id} in {total_time:.2f} seconds.")

    except Exception as e:
        total_time = time.time() - start_time
        print(f"[Pipeline] FAILED for Video ID: {video.id} after {total_time:.2f} seconds.")
        # Re-raising the exception will make the Cloud Build step fail, which is correct.
        raise


def main():
    """Command-line entry point for running the pipeline manually."""
    parser = argparse.ArgumentParser(description="Run the full video production pipeline.")
    parser.add_argument(
        "--title", type=str, required=True, help="The title of the video."
    )
    parser.add_argument(
        "--provider", type=str, default="fliki", choices=['fliki', 'pictory'], help="The video generation provider."
    )
    parser.add_argument(
        "--api_key", type=str, required=True, help="The API key for the chosen provider."
    )
    parser.add_argument(
        "--music", action="store_true", help="Add background music to the video."
    )
    args = parser.parse_args()

    # Create a mock Video object
    video_data = Video(
        id=str(uuid.uuid4()),
        title=args.title,
        description=f"A video about {args.title}"
    )

    # Create a user config object from command-line arguments
    user_config_data = UserConfig(
        video_provider=args.provider,
        provider_api_key=args.api_key,
        add_background_music=args.music
    )

    run_video_production_pipeline(video_data, user_config=user_config_data)

if __name__ == "__main__":
    main()
