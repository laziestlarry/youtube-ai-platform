from datetime import datetime, timedelta
from sqlalchemy import (Boolean, Column, Integer, String, ForeignKey, DateTime,
                        UniqueConstraint)
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

# A simplified User model for context.
# In a real app, this would have password hashes, email, etc.
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String, nullable=True)
    provider = Column(String, nullable=False, default="local")

    # Establishes the one-to-one relationship with BrandKit
    brand_kit = relationship("BrandKit", back_populates="user", uselist=False, cascade="all, delete-orphan")
    # Establishes the one-to-many relationship with video jobs
    video_jobs = relationship("VideoGenerationJob", back_populates="user")
    # Establishes the one-to-many relationship with blueprints
    blueprints = relationship("VideoBlueprint", back_populates="user", cascade="all, delete-orphan")


class BrandKit(Base):
    """
    Stores reusable branding assets for a user.
    This creates a one-to-one relationship with the User.
    """
    __tablename__ = "brand_kits"

    id = Column(Integer, primary_key=True, index=True)
    logo_path = Column(String, nullable=True) # Path to the stored logo file
    slogan = Column(String, nullable=True)
    logo_animation_path = Column(String, nullable=True) # Path to the generated logo animation (GIF/MP4)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)

    user = relationship("User", back_populates="brand_kit")


class VideoGenerationJob(Base):
    __tablename__ = "video_generation_jobs"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    status = Column(String, default="processing", index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="video_jobs")
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class VideoBlueprint(Base):
    """
    Stores a user's reusable template for a video series.
    """
    __tablename__ = "video_blueprints"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    video_provider = Column(String, default="standard")
    add_music = Column(Boolean, default=False)
    apply_brand_kit = Column(Boolean, default=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="blueprints")


class PasswordResetToken(Base):
    __tablename__ = "password_reset_tokens"

    id = Column(Integer, primary_key=True, index=True)
    token = Column(String, unique=True, index=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    expires_at = Column(DateTime, nullable=False, default=lambda: datetime.utcnow() + timedelta(hours=1))
    used = Column(Boolean, default=False, nullable=False)

    user = relationship("User")