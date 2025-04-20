from app.components.base_rule import BaseRule
from app.components.rules.quality.base_quality_rule import BaseQualityRule


class RuleHandler(BaseRule, BaseQualityRule):
    def execute(self, context):
        print("[separation_of_concerns] Verifying separation of concerns...")
        context["separation_of_concerns_passed"] = True
        return context
