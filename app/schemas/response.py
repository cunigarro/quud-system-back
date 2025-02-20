from pydantic import BaseModel
from typing import Any, Optional


class StandardResponse(BaseModel):
    message: str
    data: Optional[Any] = None
    errors: Optional[Any] = None
