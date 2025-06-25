# app/backend/worker_main.py
from fastapi import FastAPI, Depends, HTTPException, Request
from sqlalchemy.orm import Session
import json

from app.backend.db.session import get_db
from app.backend import crud
from app.full_pipeline import run_video_production_pipeline

app = FastAPI(title="YouTube AI Platform Worker")

@app.post("/process-pipeline")
async def process_pipeline_endpoint(request: Request, db: Session = Depends(get_db)):
    """
    Endpoint triggered by Google Cloud Tasks to process a video pipeline.
    """
    video_id = None # Initialize video_id to None
    try:
        # Cloud Tasks sends payload in the request body
        body = await request.json()
        video_id = body.get("video_id")
        advanced_editing = body.get("advanced_editing", False)

        if not video_id:
            raise HTTPException(status_code=400, detail="video_id is required in the payload.")

        print(f"Worker: Starting video processing for video_id: {video_id}")
        video = crud.video.get(db, id=video_id)
        if not video:
            print(f"Worker: Video with id {video_id} not found. Aborting.")
            raise HTTPException(status_code=404, detail=f"Video with id {video_id} not found.")

        crud.video.update(db, db_obj=video, obj_in={"status": "processing"})
        run_video_production_pipeline(video=video, advanced=advanced_editing)
        crud.video.update(db, db_obj=video, obj_in={"status": "completed"})
        print(f"Worker: Finished video processing for video_id: {video_id}")
        return {"status": "success", "video_id": video_id}
    except Exception as e:
        print(f"Worker: Error processing video_id {video_id}: {e}")
        if video_id: # Only attempt to update if video_id was successfully extracted
            video = crud.video.get(db, id=video_id) # Re-fetch in case of error before initial fetch
            if video: crud.video.update(db, db_obj=video, obj_in={"status": "failed"})
        raise HTTPException(status_code=500, detail=f"Error processing video: {str(e)}")

@app.get("/health")
async def health_check():
    return {"status": "ok"}