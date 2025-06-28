import os
import math
from pathlib import Path
from celery import Celery
from moviepy.editor import ImageClip, CompositeVideoClip, vfx
from sqlalchemy.orm import Session

# Assume you have a way to get a DB session in a background task
from .database import database, models


# Configure Celery to use the REDIS_URL environment variable.
# Fallback to the local redis service for docker-compose.
REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")

celery_app = Celery("tasks", broker=REDIS_URL, backend=REDIS_URL)

@celery_app.task
def start_video_pipeline(job_id: str, video_provider: str, api_key: str, scene_asset_paths: list, brand_kit: dict):
    """
    Placeholder for the main video generation pipeline.
    This would call the logic from your full_pipeline.py script.
    """
    print(f"Starting video pipeline for job {job_id} with provider {video_provider}...")
    # Here you would integrate the logic from run_video_production_pipeline
    # For now, we'll just simulate a long process.
    import time
    time.sleep(30)
    print(f"Video pipeline for job {job_id} finished.")
    # You would update the job status in the DB here.


@celery_app.task
def generate_brand_asset_preview(brand_kit_id: int):
    """
    Generates a simple 'pulse' animation from a user's logo.
    Saves it as a GIF and updates the BrandKit record in the database.
    """
    db: Session = database.SessionLocal()
    brand_kit = db.query(models.BrandKit).filter(models.BrandKit.id == brand_kit_id).first()

    if not brand_kit or not brand_kit.logo_path or not os.path.exists(brand_kit.logo_path):
        print(f"Could not generate preview for BrandKit {brand_kit_id}. Logo not found.")
        return

    try:
        print(f"Generating brand animation for BrandKit ID: {brand_kit_id}")
        logo_path = Path(brand_kit.logo_path)
        output_path = logo_path.parent / f"{logo_path.stem}_animation.gif"

        # Create a 3-second clip with a pulsing effect
        clip = ImageClip(str(logo_path), duration=3).set_position("center")
        
        # The pulse effect is a resize function applied over time
        pulse = lambda t: 1 + 0.05 * math.sin(t * 2 * math.pi)
        clip_resized = clip.fx(vfx.resize, pulse)

        # Composite onto a transparent background to ensure GIF transparency works
        final_clip = CompositeVideoClip([clip_resized], size=clip.size, bg_color=None)
        final_clip.write_gif(str(output_path), fps=15, program='ffmpeg')

        brand_kit.logo_animation_path = str(output_path)
        db.commit()
        print(f"Successfully generated and saved animation to {output_path}")
    except Exception as e:
        print(f"Error generating brand animation for BrandKit {brand_kit_id}: {e}")
    finally:
        db.close()