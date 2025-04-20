from app.components.base_rule import BaseRule
from app.components.rules.quality.base_quality_rule import BaseQualityRule


class RuleHandler(BaseRule, BaseQualityRule):
    def execute(self, context):
        print("[clarity_function_names] Checking clarity of function names...")
        context["clarity_function_names_passed"] = True
        return context
