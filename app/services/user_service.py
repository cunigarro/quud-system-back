from sqlalchemy.orm import Session

from app.repositories.user_repository import UserRepository
from app.schemas.user import (
    UserCreate, UserResponse, ProfileMetadata, UserUpdate
)
from app.core.security import create_access_token
from app.repositories.token_repository import TokenRepository


class UserService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = UserRepository(db)
        self.token_repository = TokenRepository(db)

    def register_user(self, user: UserCreate) -> UserResponse:
        try:
            db_user = self.repository.create(user)

            access_token = create_access_token(data={
                "email": db_user.email,
                "user_id": db_user.id
            })

            return {
                "user": UserResponse.from_orm(db_user),
                "access_token": access_token
            }
        except ValueError as e:
            raise Exception(f"Error registering user: {str(e)}")

    def login_user(self, email: str, password: str):
        user = self.repository.authenticate(email, password)
        if not user:
            return None

        access_token = create_access_token(data={
            "email": user.email,
            "user_id": user.id
        })

        return {"access_token": access_token, "token_type": "bearer"}

    def get_user(self, user_id: int) -> UserResponse:
        db_user = self.repository.get_by_id(user_id)
        if not db_user:
            raise ValueError("User not found")

        profile_metadata = None
        if db_user.profile_metadata:
            profile_metadata = ProfileMetadata(**db_user.profile_metadata)

        return UserResponse(
            id=db_user.id,
            names=db_user.names,
            last_names=db_user.last_names,
            cellphone=db_user.cellphone,
            email=db_user.email,
            profile_metadata=profile_metadata
        )

    def update_user(self, user_id: int, user_update: UserUpdate) -> UserResponse:
        db_user = self.repository.update(user_id, user_update)

        profile_metadata = None
        if db_user.profile_metadata:
            profile_metadata = ProfileMetadata(**db_user.profile_metadata)

        return UserResponse(
            id=db_user.id,
            names=db_user.names,
            last_names=db_user.last_names,
            cellphone=db_user.cellphone,
            email=db_user.email,
            profile_metadata=profile_metadata
        )

    def logout_user(self, token: str):
        self.token_repository.blacklist_token(token)
        return {"message": "Logout successful"}
