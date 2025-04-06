from sqlalchemy.orm import Session
from app.db.models import Inspection, InspectionStatus
from app.schemas.inspections import InspectionCreate
from app.db.enums import InspectionStatusEnum


class InspectionRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id_with_status(self, inspection_id: int):
        result = (
            self.db.query(Inspection)
            .join(InspectionStatus, Inspection.inspection_status_id == InspectionStatus.id)
            .add_columns(
                Inspection.id,
                Inspection.result,
                Inspection.processed_at,
                InspectionStatus.name.label("status_name")
            )
            .filter(Inspection.id == inspection_id, Inspection.deleted_at.is_(None))
            .first()
        )
        return result

    def create_inspection(self, inspection_data: InspectionCreate) -> Inspection:
        init_status = self.db.query(InspectionStatus).filter(
            InspectionStatus.name == InspectionStatusEnum.INIT.value
        ).first()

        if not init_status:
            raise Exception("Initial inspection status not found")

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
