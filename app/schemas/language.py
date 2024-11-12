
from uuid import UUID

from pydantic import BaseModel
from typing import List


class LanguageVersionResponse(BaseModel):
    version: str

    class Config:
        orm_mode = True


class LanguageResponse(BaseModel):
    name: str
    uuid: UUID
    versions: List[LanguageVersionResponse] = []

    class Config:
        orm_mode = True
