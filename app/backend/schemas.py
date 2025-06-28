from typing import List, Optional
from pydantic import BaseModel


# --- BrandKit Schemas ---
class BrandKitBase(BaseModel):
    slogan: Optional[str] = None
    logo_path: Optional[str] = None
    logo_animation_path: Optional[str] = None

class BrandKit(BrandKitBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True


# --- VideoBlueprint Schemas ---
class VideoBlueprintBase(BaseModel):
    name: str
    video_provider: str = "standard"
    add_music: bool = False
    apply_brand_kit: bool = True

class VideoBlueprintCreate(VideoBlueprintBase):
    pass

class VideoBlueprint(VideoBlueprintBase):
    id: int

    class Config:
        orm_mode = True

# --- User Schemas ---
class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    brand_kit: Optional[BrandKit] = None
    blueprints: List[VideoBlueprint] = []

    class Config:
        orm_mode = True

# --- Token Schemas ---
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class GoogleAuthCode(BaseModel):
    code: str

class PasswordResetRequest(BaseModel):
    email: str # Using email (username) to identify the user

class PasswordReset(BaseModel):
    token: str
    new_password: str