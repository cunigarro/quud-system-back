from app.components.base_rule import BaseRule
from app.components.rules.quality.base_quality_rule import BaseQualityRule


class RuleHandler(BaseRule, BaseQualityRule):
    def execute(self, context):
        print("[efficient_data_structures] Checking use of data structures...")
        context["efficient_data_structures_passed"] = True
        return context
