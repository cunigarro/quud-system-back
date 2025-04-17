from app.components.base_rule import BaseRule
from app.components.drivers.firebase import FirebaseDriver


class RuleHandler(BaseRule):
    def execute(self, context):
        driver = self.settings.get("driver")

        if not driver:
            raise ValueError("Missing 'driver' in settings for RuleHandler.")

        if driver == "firebase":
            print(f"Notificando vía {driver}")
            notify_driver = FirebaseDriver(context)
            context = notify_driver.execute()
        else:
            raise ValueError(f"Unsupported driver '{driver}'.")

        return context
