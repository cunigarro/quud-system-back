from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

from .rule import RuleResponse


class RuleGroupRuleResponse(BaseModel):
    id: int
    rule: RuleResponse

    class Config:
        from_attributes = True


class RuleGroupResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    owner_id: int
    group_rules: List[RuleGroupRuleResponse]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True
