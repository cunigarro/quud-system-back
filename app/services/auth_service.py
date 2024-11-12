from sqlalchemy.orm import Session

from app.repositories.user_repository import create_user, authenticate_user
from app.schemas.user import UserCreate, UserResponse
from app.core.security import create_access_token


def register_user(db: Session, user: UserCreate) -> UserResponse:
    db_user = create_user(db, user)
    return UserResponse.from_orm(db_user)


def login_user(db: Session, email: str, password: str):
    user = authenticate_user(db, email, password)
    if not user:
        return None
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}
