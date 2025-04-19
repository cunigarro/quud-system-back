from sqlalchemy.orm import Session, selectinload, joinedload

from app.db.models import Inspection, InspectionStatus
from app.schemas.inspections import InspectionCreate
from app.db.enums import InspectionStatusEnum


class InspectionRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, inspection_id: int):
        result = (
            self.db.query(Inspection)
            .options(
                selectinload(Inspection.project),
                selectinload(Inspection.owner),
                selectinload(Inspection.rule_group),
                selectinload(Inspection.status),
            )
            .filter(
                Inspection.id == inspection_id,
                Inspection.deleted_at.is_(None)
            )
            .first()
        )
        return result

    def get_by_user(self, owner_id: int, skip: int = 0, limit: int = 10):
        result = (
            self.db.query(Inspection)
            .options(
                selectinload(Inspection.project),
                selectinload(Inspection.owner),
                selectinload(Inspection.rule_group),
                selectinload(Inspection.status),
            )
            .filter(
                Inspection.owner_id == owner_id,
                Inspection.deleted_at.is_(None)
            )
            .offset(skip)
            .limit(limit)
            .all()
        )

        return result

    def create_inspection(
        self,
        inspection_data: InspectionCreate,
        owner_id
    ) -> Inspection:
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
            inspection_status_id=init_status.id,
            notification_info=inspection_data.notification_info.dict(),
            owner_id=owner_id
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

    def update_execution_info(
        self,
        inspection_id: int,
        info: dict
    ) -> Inspection:
        inspection = self.db.query(Inspection).filter(
            Inspection.id == inspection_id
        ).first()
        if not inspection:
            raise ValueError("Inspection not found")

        inspection.execution_info = info
        self.db.commit()
        self.db.refresh(inspection)
        return inspection
