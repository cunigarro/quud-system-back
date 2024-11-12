from sqlalchemy.orm import Session
from app.db.models import Language


def get_languages(db: Session):
    return db.query(Language).all()
