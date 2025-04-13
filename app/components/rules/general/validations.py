from app.components.base_rule import BaseRule


class RuleHandler(BaseRule):
    def execute(self, context):
        print("[validations] Ejecutando validaciones...")
        context["validations_passed"] = True
        return context
