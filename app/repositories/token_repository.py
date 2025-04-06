from app.db.models import TokenBlacklist
from sqlalchemy.orm import Session
from datetime import datetime


class TokenRepository:
    def __init__(self, db: Session):
        self.db = db

    def blacklist_token(self, token: str):
        token_entry = TokenBlacklist(token=token, created_at=datetime.utcnow())
        self.db.add(token_entry)
        self.db.commit()

    def is_token_blacklisted(self, token: str) -> bool:
        return self.db.query(TokenBlacklist).filter(TokenBlacklist.token == token).first() is not None
