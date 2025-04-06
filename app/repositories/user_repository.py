from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.db.models import User
from app.core.security import get_password_hash, verify_password
from app.schemas.user import UserCreate, UserUpdate


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_email(self, email: str) -> User:
        return self.db.query(User).filter(User.email == email).first()

    def get_by_id(self, user_id: int) -> User:
        return self.db.query(User).filter(User.id == user_id).first()

    def create(self, user: UserCreate) -> User:
        db_user = User(
            names=user.names,
            last_names=user.last_names,
            email=user.email,
            cellphone=user.cellphone,
            hashed_password=get_password_hash(user.password),
            profile_metadata=user.profile_metadata.dict() if user.profile_metadata else None
        )
        try:
            self.db.add(db_user)
            self.db.commit()
            self.db.refresh(db_user)
            return db_user
        except IntegrityError as e:
            raise ValueError(f"User already exists or there are duplicate data {e}.")

    def authenticate(self, email: str, password: str) -> User | None:
        user = self.get_by_email(email)
        if user and verify_password(password, user.hashed_password):
            return user
        return None

    def update(self, user_id: int, user_update: UserUpdate) -> User:
        user = self.get_by_id(user_id)
        if not user:
            raise ValueError("User not found")

        update_data = user_update.dict(exclude_unset=True)

        for field, value in update_data.items():
            if field == "profile_metadata" and value:
                value_dict = value if isinstance(value, dict) else value.dict()
                setattr(user, field, value_dict)
            else:
                setattr(user, field, value)

        self.db.commit()
        self.db.refresh(user)
        return user
