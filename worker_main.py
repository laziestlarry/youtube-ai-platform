import uvicorn
from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel

# Assuming your CRUD and DB session logic is accessible
from app.backend.db.session import SessionLocal
from app.backend import crud
from app.full_pipeline import run_video_production_pipeline

app = FastAPI(title="Video Production Worker")

class PipelineTaskPayload(BaseModel):
    video_id: int
    advanced_editing: bool = False

@app.post("/process-pipeline")
async def process_pipeline_task(payload: PipelineTaskPayload):
    """
    This endpoint is called by Google Cloud Tasks to process a single video.
    It runs the long-running video production pipeline.
    """
    print(f"Worker: Received task for video_id: {payload.video_id}")
    db = SessionLocal()
    try:
        video = crud.video.get(db, id=payload.video_id)
        if not video:
            print(f"Worker: Video with id {payload.video_id} not found. Aborting.")
            # Return 200 OK to Cloud Tasks to prevent retries for a non-existent video.
            return {"status": "error", "message": "Video not found"}

        crud.video.update(db, db_obj=video, obj_in={"status": "processing"})
        db.commit()

        run_video_production_pipeline(video=video, advanced=payload.advanced_editing)
        
        crud.video.update(db, db_obj=video, obj_in={"status": "completed"})
        db.commit()
        
        print(f"Worker: Finished video processing for video_id: {payload.video_id}")
        return {"status": "success", "video_id": payload.video_id}
    except Exception as e:
        print(f"Worker: Error processing video_id {payload.video_id}: {e}")
        video = crud.video.get(db, id=payload.video_id)
        if video:
            crud.video.update(db, db_obj=video, obj_in={"status": "failed"})
            db.commit()
        # Raise an HTTP 500 to signal to Cloud Tasks that the task failed and should be retried.
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()