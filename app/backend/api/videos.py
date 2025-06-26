from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.backend import crud, schemas
from app.backend.core.config import settings
from app.backend.db.session import get_db
from app.services import task_queue_google

router = APIRouter()


class VideoBrief(BaseModel):
    title: str
    description: Optional[str] = ""
    keywords: Optional[List[str]] = []
    commercial_angle: Optional[str] = ""
    source: Optional[str] = "mini-app"


@router.post("/initiate-from-brief/", response_model=schemas.VideoInDB)
def initiate_video_from_brief(
    *,
    db: Session = Depends(get_db),
        brief: VideoBrief):
    """
    Receives a brief from the mini-app, creates a video record,
    and triggers the background pipeline.
    """
    # For now, we'll hardcode channel and creator IDs.
    # In a real app, this would come from the authenticated user.
    video_in = schemas.VideoCreate(
        title=brief.title,
        description=brief.description,
        channel_id=1,
        creator_id=1,
        status="queued",
    )
    video = crud.video.create(db=db, obj_in=video_in)

    # Trigger the background worker via Google Cloud Tasks
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
            detail="Server bad configed (missing GCP/Cloud Tasks settings).",
        )
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


@router.get("/{video_id}", response_model=schemas.VideoInDB)
def get_video(*, db: Session = Depends(get_db), video_id: int):
    video = crud.video.get(db, id=video_id)
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    return video
