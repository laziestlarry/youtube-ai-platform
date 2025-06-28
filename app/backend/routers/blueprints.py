from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import schemas
from ..database import models
from ..dependencies import get_db, get_current_user

router = APIRouter()

@router.get("/blueprints", response_model=List[schemas.VideoBlueprint])
def get_user_blueprints(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Retrieve all blueprints for the current user."""
    return db.query(models.VideoBlueprint).filter(models.VideoBlueprint.user_id == current_user.id).all()

@router.post("/blueprints", response_model=schemas.VideoBlueprint, status_code=status.HTTP_201_CREATED)
def create_blueprint(
    blueprint: schemas.VideoBlueprintCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Create a new blueprint for the current user."""
    db_blueprint = models.VideoBlueprint(**blueprint.dict(), user_id=current_user.id)
    db.add(db_blueprint)
    db.commit()
    db.refresh(db_blueprint)
    return db_blueprint

@router.delete("/blueprints/{blueprint_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_blueprint(
    blueprint_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Delete a blueprint belonging to the current user."""
    db_blueprint = db.query(models.VideoBlueprint).filter(models.VideoBlueprint.id == blueprint_id).first()
    if not db_blueprint or db_blueprint.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blueprint not found")
    db.delete(db_blueprint)
    db.commit()
    return