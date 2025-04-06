from enum import Enum


class InspectionStatusEnum(str, Enum):
    INIT = "init"
    PROCESSING = "processing"
    COMPLETED = "completed"
    ERROR = "error"
