from typing import List, Optional

from pydantic import BaseModel


class VideoBase(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: str = "draft"


class VideoCreate(VideoBase):
    title: str
    channel_id: int
    creator_id: int


class VideoUpdate(VideoBase):
    pass


class VideoInDB(VideoCreate):
    id: int

    class Config:
        orm_mode = True
