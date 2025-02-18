from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.db.models import User
from app.core.security import get_password_hash, verify_password
from app.schemas.user import UserCreate


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, user: UserCreate):
    db_user = User(
        names=user.names,
        last_names=user.last_names,
        email=user.email,
        cellphone=user.cellphone,
        hashed_password=get_password_hash(user.password),
    )
    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except IntegrityError as e:
        raise ValueError(f"User already exists or there are duplicate data {e}.")


def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if user and verify_password(password, user.hashed_password):
        return user
    return None
