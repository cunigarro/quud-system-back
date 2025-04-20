from pydantic import BaseModel, model_validator
from typing import Optional, List, Any
from datetime import datetime

from app.db.enums import RuleDimensionEnum


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


class WeigthType(BaseModel):
    rule_type_id: int
    quantity: float

    class Config:
        from_attributes = True


class RuleGroupCreate(BaseModel):
    name: str
    description: Optional[str]
    rule_ids: List[int]
    attributes_weights: List[WeigthType]
    paradigm_weights: List[WeigthType]
    alfa: float

    @model_validator(mode="after")
    def check_weights_sum_to_one(self):
        total = sum(w.quantity for w in self.attributes_weights)
        if abs(total - 1.0) >= 1e-6:
            raise ValueError(
                f'The sum of the weights of attributes should be exactly 1.0, but it was {total}'
            )

        total = sum(w.quantity for w in self.paradigm_weights)
        if abs(total - 1.0) >= 1e-6:
            raise ValueError(
                f'The sum of the weights of paradigm should be exactly 1.0, but it was {total}'
            )

        return self


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
    dimension: RuleDimensionEnum

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
