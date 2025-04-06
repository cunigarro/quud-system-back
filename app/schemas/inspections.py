from pydantic import BaseModel
from typing import Optional, Any
from datetime import datetime


class InspectionCreate(BaseModel):
    branch: str
    project_id: int
    rule_group_id: Optional[int] = None


class InspectionResponse(BaseModel):
    id: int
    branch: str
    project_id: int
    rule_group_id: Optional[int]
    created_at: datetime

    class Config:
        from_attributes = True


class InspectionDetailResponse(BaseModel):
    id: int
    status: str
    processed_at: Optional[datetime]
    result: Optional[Any]

    class Config:
        from_attributes = True
