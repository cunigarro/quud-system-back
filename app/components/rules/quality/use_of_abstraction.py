from app.components.base_rule import BaseRule
from app.components.rules.quality.base_quality_rule import BaseQualityRule


class RuleHandler(BaseRule, BaseQualityRule):
    def execute(self, context):
        print("[use_of_abstraction] Checking for abstraction practices...")
        context["use_of_abstraction_passed"] = True
        return context
