from datetime import datetime
from typing import Optional

from pydantic import BaseModel, HttpUrl


class ProjectBase(BaseModel):
    name: str
    url: HttpUrl
    language_id: Optional[int] = None
    language_version_id: Optional[int] = None


class ProjectCreate(ProjectBase):
    pass


class ProjectResponse(ProjectBase):
    id: int
    owner_id: int
    url: HttpUrl
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime]

    class Config:
        from_attributes = True
