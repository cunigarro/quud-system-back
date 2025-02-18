from pydantic import BaseModel, EmailStr
from typing import Optional


class UserCreate(BaseModel):
    names: str
    last_names: str
    cellphone: Optional[str] = None
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    id: int
    names: str
    last_names: str
    email: EmailStr

    class Config:
        from_attributes = True
