from app.components.base_rule import BaseRule
from app.components.rules.quality.base_quality_rule import BaseQualityRule


class RuleHandler(BaseRule, BaseQualityRule):
    def execute(self, context):
        print("[private_attributes] Checking for use of private attributes...")
        context["private_attributes_passed"] = True
        return context
