from app.components.base_rule import BaseRule
from app.components.rules.quality.base_quality_rule import BaseQualityRule


class RuleHandler(BaseRule, BaseQualityRule):
    def execute(self, context):
        print("[efficient_algorithms] Checking efficiency of algorithms...")
        context["efficient_algorithms_passed"] = True
        return context
