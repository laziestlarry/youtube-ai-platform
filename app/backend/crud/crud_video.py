from .base import CRUDBase
from app.backend.models.video import Video
from app.backend.schemas.video import VideoCreate, VideoUpdate

class CRUDVideo(CRUDBase[Video, VideoCreate, VideoUpdate]):
    pass

video = CRUDVideo(Video)