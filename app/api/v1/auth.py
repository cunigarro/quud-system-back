from fastapi import APIRouter, Depends, Form
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.user import UserCreate
from app.services.auth_service import register_user, login_user
from app.schemas.response import StandardResponse

router = APIRouter()


@router.post("/api/register", response_model=StandardResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    try:
        user_data = register_user(db, user)
        return StandardResponse(
            message="User registered successfully",
            data=user_data
        )
    except Exception as e:
        return StandardResponse(
            message="User registration failed",
            errors=str(e)
        )


@router.post("/api/login", response_model=StandardResponse)
def login(username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    token = login_user(db, username, password)
    if not token:
        return StandardResponse(
            message="Invalid credentials", 
            errors="Invalid credentials"
        )
    return StandardResponse(
        message="Login successful",
        data={"token": token}
    )
