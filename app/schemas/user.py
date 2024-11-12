from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    names: str
    last_names: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: str
    password: str


class UserResponse(BaseModel):
    id: int
    names: str
    last_names: str
    email: EmailStr

    class Config:
        orm_mode = True
