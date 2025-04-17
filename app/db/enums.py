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

    @classmethod
    def get_value_from_id(cls, id: int):
        reverse_mapping = {
            1: cls.INIT,
            2: cls.PROCESSING,
            3: cls.COMPLETED,
            4: cls.ERROR
        }
        return reverse_mapping.get(id, None)
