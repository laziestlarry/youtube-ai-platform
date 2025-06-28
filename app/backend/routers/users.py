from fastapi import APIRouter, Depends

from .. import schemas
from ..database import models
from ..dependencies import get_current_user

router = APIRouter()

@router.get("/users/me", response_model=schemas.User)
def read_users_me(current_user: models.User = Depends(get_current_user)):
    """
    Get the full profile for the current logged-in user,
    including their brand kit and blueprints.
    """
    return current_user