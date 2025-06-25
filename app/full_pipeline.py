from app.backend.models.video import Video
from app.backend.core.config import settings
from app.services.script_generator_vertex import generate_script_with_gemini
from app.services.tts_google import synthesize_speech_google
from app.services.gcs_utils import upload_to_gcs # Assumes a new utility for GCS
from app.services.video_assembler_ffmpeg import assemble_video
from app.services.youtube_uploader import upload_to_youtube

def run_video_production_pipeline(video: Video, advanced=False):
    """
    Executes the full video production pipeline for a given video record.
    This function should be triggered by a background worker (e.g., Celery, Cloud Tasks).
    """
    print(f"[Pipeline] Starting for Video ID: {video.id}, Title: {video.title}")

    # 1. Generate Script using Vertex AI
    script = generate_script_with_gemini(video.title, video.description)
    print(f"[Pipeline] Generated script for Video ID {video.id}")

    # 2. Synthesize Speech using Google Cloud TTS
    # This should return the audio content in-memory
    audio_content = synthesize_speech_google(script)
    audio_blob_name = f"videos/{video.id}/generated_audio.mp3"
    
    # 3. Upload audio to Google Cloud Storage
    audio_gcs_uri = upload_to_gcs(audio_content, settings.GCS_BUCKET_NAME, audio_blob_name)
    print(f"[Pipeline] Synthesized audio and uploaded to: {audio_gcs_uri}")

    # ... Subsequent steps (video assembly using the GCS URI, upload) would follow ...

    print(f"[Pipeline] Pipeline complete for Video ID: {video.id}.")