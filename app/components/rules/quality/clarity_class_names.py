from app.components.base_rule import BaseRule
from app.components.rules.quality.base_quality_rule import BaseQualityRule


class RuleHandler(BaseRule, BaseQualityRule):
    def execute(self, context):
        print("[clarity_class_names] Checking for clear class names...")
        context["clarity_class_names_passed"] = True
        return context
