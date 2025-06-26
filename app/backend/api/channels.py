from typing import List

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

# In-memory storage for demonstration
channels_db = {}


class ChannelCreate(BaseModel):
    name: str
    description: str = ""
    owner_id: int


class ChannelOut(ChannelCreate):
    id: int


@router.get("/", response_model=List[ChannelOut])
def list_channels():
    return list(channels_db.values())


@router.post("/", response_model=ChannelOut)
def create_channel(channel: ChannelCreate):
    channel_id = len(channels_db) + 1
    channel_out = ChannelOut(id=channel_id, **channel.dict())
    channels_db[channel_id] = channel_out
    return channel_out


@router.get("/{channel_id}", response_model=ChannelOut)
def get_channel(channel_id: int):
    channel = channels_db.get(channel_id)
    if not channel:
        raise HTTPException(status_code=404, detail="Channel not found")
    return channel
