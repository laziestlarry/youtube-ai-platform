from typing import Optional

from pydantic import BaseModel, EmailStr


# Shared properties
class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = True
    username: Optional[str] = None


# Properties to receive via API on creation
class UserCreate(UserBase):
    email: EmailStr
    password: str
    username: str


# Properties to receive via API on update
class UserUpdate(UserBase):
    password: Optional[str] = None


# Properties shared by models stored in DB
class UserInDBBase(UserBase):
    id: int

    class Config:
        orm_mode = True
