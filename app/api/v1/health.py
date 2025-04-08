from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.response import StandardResponse

router = APIRouter()


@router.get("/", response_model=StandardResponse)
def get_languages(db: Session = Depends(get_db)):
    return StandardResponse(
        message="Service running",
        data={
            'doc': '/docs'
        }
    )
