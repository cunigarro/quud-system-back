from sqlalchemy.orm import Session

from app.components.base_rule import BaseRule
from app.db.enums import RuleDimensionEnum
from app.schemas.rule import WeigthType
from app.repositories.inspection_rule_repository import (
    InspectionRuleRepository
)


class RuleHandler(BaseRule):

    def calculate_dimension(self, db: Session, weights: list, dimension: str, inspection_id: int) -> float:
        sum_weights = 0.0
        score = 0.0

        for weight in weights:
            weight = WeigthType(**weight)
            avg_calification = InspectionRuleRepository.get_avg_calification_by_dimension(
                db=db,
                inspection_id=inspection_id,
                rule_type_id=weight.rule_type_id,
                dimension=dimension
            )

            if avg_calification is not None:
                sum_weights += weight.quantity
                score += weight.quantity * avg_calification

        return score / sum_weights if sum_weights != 0 else 0.0

    def execute(self, context):
        inspection = context['inspection']

        group_rule = inspection.rule_group
        alfa = group_rule.alfa

        total_attributes = self.calculate_dimension(
            context["db"],
            group_rule.attributes_weights,
            RuleDimensionEnum.attribute.value,
            inspection.id
        )
        total_paradigm = self.calculate_dimension(
            context["db"],
            group_rule.paradigm_weights,
            RuleDimensionEnum.paradigm.value,
            inspection.id
        )

        total_score = alfa * total_attributes + (1 - alfa) * total_paradigm

        inspection.total_score = total_score
        inspection.total_paradigm = total_paradigm
        inspection.total_attributes = total_attributes

        context["db"].commit()

        return context
