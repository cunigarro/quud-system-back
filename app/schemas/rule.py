from pydantic import BaseModel
from typing import Optional, List, Any
from datetime import datetime


class RuleTypeSchema(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class RuleSchema(BaseModel):
    id: int
    name: str
    description: str
    flow_config: Optional[dict]
    rule_type: RuleTypeSchema

    class Config:
        from_attributes = True


class RuleGroupCreate(BaseModel):
    name: str
    description: Optional[str]
    rule_ids: List[int]


class RuleGroupSchema(BaseModel):
    id: int
    name: str
    description: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


class RuleTypeResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class RuleResponse(BaseModel):
    id: int
    name: str
    description: str
    rule_type: Optional[RuleTypeResponse]
    flow_config: Optional[Any]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True
