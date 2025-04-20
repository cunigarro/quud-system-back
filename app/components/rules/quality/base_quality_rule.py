from app.schemas.inspections import Comment
from app.repositories.inspection_rule_repository import (
    InspectionRuleRepository
)


class BaseQualityRule:
    def get_path(self, context):
        return context['data']['fetch_code']['repository_path']

    def save_quality_result(
        self,
        context,
        calification: float,
        comments: list[Comment],
        message: str,
        details: dict,
    ):
        inspection = context['inspection']
        rule_id = context['rule_id']

        InspectionRuleRepository.upsert_inspection_rule(
            context['db'],
            inspection.id,
            rule_id,
            calification,
            message,
            details,
            [comment.dict() for comment in comments],
        )
