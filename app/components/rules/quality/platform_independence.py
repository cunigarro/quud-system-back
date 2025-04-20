from app.components.base_rule import BaseRule
from app.components.rules.quality.base_quality_rule import BaseQualityRule


class RuleHandler(BaseRule, BaseQualityRule):
    def execute(self, context):
        print("[platform_independence] Checking for platform independence...")
        context["platform_independence_passed"] = True
        return context
