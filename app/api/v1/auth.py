from fastapi import APIRouter, Depends, Form
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.user import UserCreate, UserUpdate
from app.services.user_service import UserService
from app.core.security import get_current_user
from app.schemas.response import StandardResponse

router = APIRouter()


@router.post("/api/register", response_model=StandardResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    try:
        user_data = UserService(db).register_user(user)
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
    token = UserService(db).login_user(username, password)
    if not token:
        return StandardResponse(
            message="Invalid credentials",
            errors="Invalid credentials"
        )
    return StandardResponse(
        message="Login successful",
        data={"token": token}
    )


@router.get("/user/profile", response_model=StandardResponse)
def get_user(db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    try:
        return StandardResponse(
            message="Successful user fetched.",
            data={"user": UserService(db).get_user(current_user.id)}
        )
    except Exception as e:
        return StandardResponse(
            message="User fetched failed",
            errors=str(e)
        )


@router.put("/profile", response_model=StandardResponse)
def update_user(
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    try:
        updated_user = UserService(db).update_user(current_user.id, user_update)
        return StandardResponse(
            message="User updated successfully.",
            data={"user": updated_user}
        )
    except Exception as e:
        return StandardResponse(
            message="User update failed.",
            errors=str(e)
        )
