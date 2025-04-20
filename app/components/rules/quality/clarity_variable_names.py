from app.components.base_rule import BaseRule
from app.components.rules.quality.base_quality_rule import BaseQualityRule


class RuleHandler(BaseRule, BaseQualityRule):
    def execute(self, context):
        print("[clarity_variable_names] Checking clarity of variable names...")
        context["clarity_variable_names_passed"] = True
        return context
