from app.components.base_rule import BaseRule


class RuleHandler(BaseRule):
    def execute(self, context):
        print(f"Notificando vía {self.settings.get('driver')}")
        return context
