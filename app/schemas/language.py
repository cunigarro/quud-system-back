
from uuid import UUID

from pydantic import BaseModel
from typing import List


class LanguageVersionResponse(BaseModel):
    version: str

    class Config:
        from_attributes = True


class LanguageResponse(BaseModel):
    name: str
    uuid: UUID
    versions: List[LanguageVersionResponse] = []

    class Config:
        from_attributes = True
