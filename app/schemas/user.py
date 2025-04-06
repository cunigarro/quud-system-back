from pydantic import BaseModel, EmailStr
from typing import Optional


class ProfileMetadata(BaseModel):
    profile_photo: str
    name_profile: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    status_description: Optional[str] = None


class UserUpdate(BaseModel):
    names: Optional[str] = None
    last_names: Optional[str] = None
    cellphone: Optional[str] = None
    email: Optional[EmailStr] = None
    profile_metadata: Optional[ProfileMetadata] = None


class UserCreate(BaseModel):
    names: str
    last_names: str
    cellphone: Optional[str] = None
    email: EmailStr
    password: str
    profile_metadata: Optional[ProfileMetadata] = None


class LoginRequest(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    id: int
    names: str
    last_names: str
    email: EmailStr
    profile_metadata: Optional[ProfileMetadata] = None

    class Config:
        from_attributes = True
