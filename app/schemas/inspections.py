from typing import Optional, Any, List
from datetime import datetime


from pydantic import BaseModel

from .user import UserResponse
from .rule_group import RuleGroupResponse
from .project import ProjectResponse


class NotificationInspection(BaseModel):
    firebase_token: str = ''


class InspectionCreate(BaseModel):
    branch: str
    project_id: int
    rule_group_id: Optional[int] = None
    notification_info: Optional[NotificationInspection] = None


class InspectionResponse(BaseModel):
    id: int
    branch: str
    project_id: int
    rule_group_id: Optional[int]
    created_at: datetime
    error: Optional[str] = None

    class Config:
        from_attributes = True


class StatusResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class Comment(BaseModel):
    line_start: Optional[str] = None
    line_end: Optional[str] = None
    path_file: str
    description: str


class InspectionRuleResponse(BaseModel):
    id: int
    calification: Optional[float]
    comments: Optional[List[Comment]]
    details: Optional[Any] = None
    message: Optional[str] = None

    class Config:
        from_attributes = True


class InspectionDetailResponse(BaseModel):
    id: int
    status: StatusResponse
    project: ProjectResponse
    owner: UserResponse
    rule_group: Optional[RuleGroupResponse]
    processed_at: Optional[datetime]
    total_score: float
    total_attributes: float
    total_paradigm: float
    validations: Optional[Any] = None
    error: Optional[str] = None
    execution_info: Optional[Any]
    history_status: Optional[Any]
    inspection_rules: List[InspectionRuleResponse]

    class Config:
        from_attributes = True
