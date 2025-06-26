from typing import List

from core.event_bus import event_bus
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

tasks_db = {}


class TaskCreate(BaseModel):
    video_id: int
    assigned_to: int  # user or agent id
    type: str  # e.g., 'script', 'edit', 'upload'
    status: str = "pending"


class TaskOut(TaskCreate):
    id: int


@router.get("/", response_model=List[TaskOut])
def list_tasks():
    return list(tasks_db.values())


@router.post("/", response_model=TaskOut)
def create_task(task: TaskCreate):
    task_id = len(tasks_db) + 1
    task_out = TaskOut(id=task_id, **task.dict())
    tasks_db[task_id] = task_out
    # Publish event for workflow automation
    event_bus.publish("TaskCreated", task_out.dict())
    return task_out


@router.get("/{task_id}", response_model=TaskOut)
def get_task(task_id: int):
    task = tasks_db.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task
