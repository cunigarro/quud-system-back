from sqlalchemy.orm import Session

from app.db.models import Inspection, InspectionStatus
from app.schemas.inspections import InspectionCreate
from app.db.enums import InspectionStatusEnum
from sqlalchemy.orm import joinedload


class InspectionRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id_with_status(self, inspection_id: int):
        result = (
            self.db.query(Inspection)
            .join(
                InspectionStatus,
                Inspection.inspection_status_id == InspectionStatus.id
            )
            .add_columns(
                Inspection.id,
                Inspection.result,
                Inspection.execution_info,
                Inspection.processed_at,
                InspectionStatus.name.label("status_name")
            )
            .filter(
                Inspection.id == inspection_id,
                Inspection.deleted_at.is_(None)
            )
            .first()
        )
        return result

    def create_inspection(self, inspection_data: InspectionCreate) -> Inspection:
        init_status = self.db.query(InspectionStatus).filter(
            InspectionStatus.name == InspectionStatusEnum.INIT.value
        ).first()

        if not init_status:
            raise ValueError(
                "Initial inspection status not found"
            )

        new_inspection = Inspection(
            branch=inspection_data.branch,
            project_id=inspection_data.project_id,
            rule_group_id=inspection_data.rule_group_id,
            inspection_status_id=init_status.id
        )
        self.db.add(new_inspection)
        self.db.commit()
        self.db.refresh(new_inspection)
        return new_inspection

    def get_inspection_with_group(self, inspection_id: int) -> Inspection:
        return (
            self.db.query(Inspection)
            .options(joinedload(Inspection.rule_group))
            .filter(Inspection.id == inspection_id)
            .first()
        )

    def update_execution_info(self, inspection_id: int, info: dict) -> Inspection:
        inspection = self.db.query(Inspection).filter(
            Inspection.id == inspection_id
        ).first()
        if not inspection:
            raise ValueError("Inspection not found")

        inspection.execution_info = info
        self.db.commit()
        self.db.refresh(inspection)
        return inspection
