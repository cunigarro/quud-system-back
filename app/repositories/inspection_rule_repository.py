from sqlalchemy.orm import Session
from sqlalchemy import func

from typing import List, Optional

from app.db.models import InspectionRule, Rule, RuleType
from app.schemas.inspections import Comment


class InspectionRuleRepository:

    @staticmethod
    def get_avg_calification_by_dimension(
        db: Session,
        inspection_id: int,
        rule_type_id: int,
        dimension: str
    ) -> float:
        return (
            db.query(func.avg(InspectionRule.calification))
            .join(Rule, Rule.id == InspectionRule.rule_id)
            .join(RuleType, RuleType.id == Rule.rule_type_id)
            .filter(InspectionRule.inspection_id == inspection_id)
            .filter(Rule.rule_type_id == rule_type_id)
            .filter(RuleType.dimension == dimension)
            .scalar()
        )

    @staticmethod
    def upsert_inspection_rule(
        db: Session,
        inspection_id: int,
        rule_id: int,
        calification: float,
        message: str,
        details: dict,
        comments: Optional[List[Comment]] = None
    ) -> InspectionRule:
        instance = db.query(InspectionRule).filter_by(
            inspection_id=inspection_id,
            rule_id=rule_id
        ).first()

        comments_data = [
            comment.dict() for comment in comments
        ] if comments else []

        if instance:
            instance.calification = calification
            instance.comments = comments_data
            instance.details = details
            instance.message = message
        else:
            instance = InspectionRule(
                inspection_id=inspection_id,
                rule_id=rule_id,
                calification=calification,
                comments=comments_data,
                message=message,
                details=details
            )
            db.add(instance)

        db.commit()
        db.refresh(instance)
        return instance
