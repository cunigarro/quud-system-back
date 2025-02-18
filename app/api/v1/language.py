from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.services.language_service import fetch_languages
from app.schemas.language import LanguageResponse

router = APIRouter()


@router.get("/languages", response_model=List[LanguageResponse])
def get_languages(db: Session = Depends(get_db)):
    return fetch_languages(db)
