from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.backend import crud, schemas
from app.backend.api import deps
from app.backend.core.config import settings
from app.services import task_queue_google

router = APIRouter()


@router.post("/generate", response_model=schemas.Video)
def generate_video(
    *,
    db: Session = Depends(deps.get_db),
    video_in: schemas.VideoCreate,
    # current_user: models.User = Depends(deps.get_current_active_user), #
    # Optional: secure endpoint
) -> any:
    """
    Create a new video record and enqueue a task for the worker to generate it.
    """
    # 1. Create the video record in the database with a "pending" status
    video = crud.video.create(db=db, obj_in=video_in)

    # 2. Validate that all required configuration for task creation is present
    required_configs = [
        settings.GCP_PROJECT_ID,
        settings.TASK_QUEUE_NAME,
        settings.TASK_QUEUE_LOCATION,
        settings.WORKER_URL,
        settings.WORKER_SA_EMAIL,
    ]
    if not all(required_configs):
        raise HTTPException(
            status_code=500,
            detail="Server is not configured for background video processing.",
        )

    # 3. Create a task in the Google Cloud Tasks queue
    payload = {"video_id": video.id, "advanced_editing": False}
    task_queue_google.create_http_task(
        project=settings.GCP_PROJECT_ID,
        queue=settings.TASK_QUEUE_NAME,
        location=settings.TASK_QUEUE_LOCATION,
        url=f"{settings.WORKER_URL}/process-pipeline",
        payload=payload,
        service_account_email=settings.WORKER_SA_EMAIL,
    )

    return video
