
from uuid import UUID

from pydantic import BaseModel
from typing import List


class LanguageVersionResponse(BaseModel):
    version: str
    id: int

    class Config:
        from_attributes = True


class LanguageResponse(BaseModel):
    id: int
    name: str
    uuid: UUID
    versions: List[LanguageVersionResponse] = []

    class Config:
        from_attributes = True
