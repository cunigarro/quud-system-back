from fastapi import APIRouter, Depends
from fastapi import Query
from sqlalchemy.orm import Session

from app.schemas.inspections import InspectionCreate, InspectionDetailResponse
from app.services.inspection_service import InspectionService
from app.db.database import get_db
from app.core.security import get_current_user
from app.schemas.response import StandardResponse

router = APIRouter()


@router.post("/", response_model=StandardResponse)
def create_inspection(
    data: InspectionCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    inspection = InspectionService(db).create_inspection(data, current_user.id)
    return StandardResponse(
        message="Inspection created successfully",
        data={"inspection": inspection}
    )


@router.get("/{inspection_id}", response_model=StandardResponse)
def get_inspection(
    inspection_id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user)
):
    try:
        inspection = InspectionService(db).get_inspection_by_id(
            inspection_id
        )
        return StandardResponse(
            message="Inspection fetched successfully",
            data={"inspection": inspection}
        )
    except Exception as e:
        return StandardResponse(
            message="Failed to fetch inspection",
            errors=str(e)
        )


@router.get("/", response_model=StandardResponse)
def get_inspections_by_user(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1),
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user)
):
    try:
        inspections = InspectionService(db).get_inspection_by_user(
            current_user.id,
            skip=skip,
            limit=limit
        )
        return StandardResponse(
            message="Inspections fetched successfully",
            data={"inspections": inspections}
        )
    except Exception as e:
        return StandardResponse(
            message="Failed to fetch inspection",
            errors=str(e)
        )
