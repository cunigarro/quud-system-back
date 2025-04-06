from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class RuleGroupResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    owner_id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True
