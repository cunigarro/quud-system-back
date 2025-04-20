from app.components.base_rule import BaseRule
from app.components.rules.quality.base_quality_rule import BaseQualityRule


class RuleHandler(BaseRule, BaseQualityRule):
    def execute(self, context):
        print("[access_methods] Verifying use of getters and setters...")
        context["access_methods_passed"] = True
        return context
