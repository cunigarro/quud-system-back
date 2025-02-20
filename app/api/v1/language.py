from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.services.language_service import fetch_languages
from app.schemas.response import StandardResponse

router = APIRouter()


@router.get("/languages", response_model=StandardResponse)
def get_languages(db: Session = Depends(get_db)):
    languages = fetch_languages(db)
    return StandardResponse(
        message="Languages fetched successfully",
        data=languages
    )
