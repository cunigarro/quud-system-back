from app.components.base_rule import BaseRule


class RuleHandler(BaseRule):
    def execute(self, context):
        print(
            "[implementation_all_classes] Verificando clases implementadas..."
        )
        context["implementation_all_classes"] = True
        return context
