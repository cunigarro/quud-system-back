from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.user import UserCreate, UserLogin, UserResponse
from app.services.auth_service import register_user, login_user

router = APIRouter()


@router.post("/api/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    return register_user(db, user)


@router.post("/api/login")
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    token = login_user(db, user_data.email, user_data.password)
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    return token
