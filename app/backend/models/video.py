from sqlalchemy import Column, String, Text

from app.backend.db.base_class import Base


class Video(Base):
    __tablename__ = "videos"

    id = Column(String, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String, default="pending", nullable=False)
    gcs_audio_uri = Column(String, nullable=True)