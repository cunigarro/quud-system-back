from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.schemas.inspections import InspectionCreate, InspectionResponse
from app.repositories.inspection_repository import InspectionRepository


class InspectionService:
    def __init__(self, db: Session):
        self.repository = InspectionRepository(db)

    def create_inspection(self, data: InspectionCreate) -> InspectionResponse:
        try:
            inspection = self.repository.create_inspection(data)
            return InspectionResponse.from_orm(inspection)
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Inspection creation failed: {str(e)}")

    def get_inspection_by_id(self, inspection_id: int):
        inspection = self.repository.get_by_id_with_status(inspection_id)

        if not inspection:
            raise ValueError("Inspection not found")

        return {
            "id": inspection.id,
            "status": inspection.status_name,
            "processed_at": inspection.processed_at,
            "result": inspection.result,
        }