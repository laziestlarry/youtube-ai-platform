from fastapi import APIRouter, HTTPException, Depends
from typing import List
from sqlalchemy.orm import Session

from app.backend import crud, schemas
from app.backend.db.session import get_db

router = APIRouter()

@router.get("/", response_model=List[schemas.UserInDBBase])
def list_users(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    """
    Retrieve users.
    """
    users = crud.user.get_multi(db, skip=skip, limit=limit)
    return users

@router.post("/", response_model=schemas.UserInDBBase)
def create_user(*, db: Session = Depends(get_db), user_in: schemas.UserCreate):
    """
    Create new user.
    """
    user = crud.user.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system.",
        )
    user = crud.user.create(db, obj_in=user_in)
    return user

@router.get("/{user_id}", response_model=schemas.UserInDBBase)
def get_user(*, db: Session = Depends(get_db), user_id: int):
    user = crud.user.get(db, id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user