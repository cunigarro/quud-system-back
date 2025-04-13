from datetime import datetime
from app.db.enums import InspectionStatusEnum
from .base import BaseDriver


class PushStateDriver(BaseDriver):
    def execute(self, context):
        inspection = context.get("inspection")
        if not inspection:
            raise ValueError("Missing inspection in context")

        state = self.settings.get("state")
        if not state:
            raise ValueError("Missing 'state' in settings for push_state.")

        try:
            status_enum = InspectionStatusEnum(state)
        except ValueError:
            states = [e.value for e in InspectionStatusEnum]
            raise ValueError(
                f"Invalid state '{state}'. Use one of: {states}"
            )

        inspection.inspection_status_id = status_enum.get_id()

        new_entry = {
            "state": status_enum.value,
            "updated_at": datetime.utcnow().isoformat()
        }

        history = inspection.history_status or []
        history.append(new_entry)
        inspection.history_status = history

        inspection_id = status_enum.get_id()
        print(
            f"[push_state] Inspection updated to '{state}' ID {inspection_id}"
        )

        context["db"].commit()

        return context
