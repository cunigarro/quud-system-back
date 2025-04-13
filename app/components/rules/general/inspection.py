from app.components.base_rule import BaseRule
from app.components.drivers.push_state import PushStateDriver


class RuleHandler(BaseRule):
    def execute(self, context):
        driver_name = self.settings.get("driver")

        if driver_name == "push_state":
            driver = PushStateDriver(self.settings)
        else:
            raise ValueError(f"Driver '{driver_name}' not implemented.")

        return driver.execute(context)
