from enum import Enum


class InspectionStatusEnum(str, Enum):
    INIT = "init"
    PROCESSING = "processing"
    COMPLETED = "completed"
    ERROR = "error"

    def get_id(self):
        mapping = {
            "init": 1,
            "processing": 2,
            "completed": 3,
            "error": 4
        }
        return mapping.get(self.value, None)
