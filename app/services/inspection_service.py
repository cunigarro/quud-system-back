from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.schemas.inspections import (
    InspectionCreate,
    InspectionResponse,
    InspectionDetailResponse
)
from app.repositories.inspection_repository import InspectionRepository
from app.components.orchestrator import Orchestrator


class InspectionService:
    def __init__(self, db: Session):
        self.repository = InspectionRepository(db)
        self.db = db

    def create_inspection(
        self, data: InspectionCreate,
        owner_id
    ) -> InspectionResponse:
        inspection = None
        try:
            inspection = self.repository.create_inspection(data, owner_id)
            inspection = self.repository.get_inspection_with_group(
                inspection.id
            )

            orchestrator = Orchestrator(self.db, inspection)
            execution_info = orchestrator.execute_inspection()

            inspection = self.repository.update_execution_info(
                inspection.id,
                execution_info
            )

            return InspectionResponse.from_orm(inspection)
        except Exception as e:
            if inspection:
                result = {
                    "steps": [],
                    "success": False,
                    "error": str(e)
                }
                inspection = self.repository.update_execution_info(
                    inspection.id,
                    result
                )

            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Inspection creation failed: {str(e)}"
            )

    def get_inspection_by_id(self, inspection_id: int):
        inspection = self.repository.get_by_id(inspection_id)

        if not inspection:
            raise ValueError("Inspection not found")

        return InspectionDetailResponse.from_orm(inspection)

    def get_inspection_by_user(
        self,
        inspection_id: int,
        skip: int = 0,
        limit: int = 10
    ):
        inspections = self.repository.get_by_user(
            inspection_id,
            skip=skip,
            limit=limit
        )
        result = [
            InspectionDetailResponse.from_orm(model) for model in inspections
        ]
        return result
