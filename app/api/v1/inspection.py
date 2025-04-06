from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.inspections import InspectionCreate, InspectionDetailResponse
from app.services.inspection_service import InspectionService
from app.db.database import get_db
from app.core.security import get_current_user
from app.schemas.response import StandardResponse

router = APIRouter()


@router.post("/inspections", response_model=StandardResponse)
def create_inspection(
    data: InspectionCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    inspection = InspectionService(db).create_inspection(data)
    return StandardResponse(
        message="Inspection created successfully",
        data={"inspection": inspection}
    )


@router.get("/inspections/{inspection_id}", response_model=StandardResponse)
def get_inspection(
    inspection_id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user)
):
    try:
        inspection_data = InspectionService(db).get_inspection_by_id(inspection_id)
        return StandardResponse(
            message="Inspection fetched successfully",
            data={"inspection": InspectionDetailResponse(**inspection_data)}
        )
    except Exception as e:
        return StandardResponse(
            message="Failed to fetch inspection",
            errors=str(e)
        )