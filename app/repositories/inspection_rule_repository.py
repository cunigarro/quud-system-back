from sqlalchemy.orm import Session
from sqlalchemy import func

from app.db.models import InspectionRule, Rule, RuleType


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
