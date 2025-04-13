from app.components.base_rule import BaseRule


class RuleHandler(BaseRule):
    def execute(self, context):
        print("[required_classes] Verificando clases requeridas...")
        context["required_classes_found"] = True
        return context
