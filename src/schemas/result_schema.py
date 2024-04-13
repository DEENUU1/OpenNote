from pydantic import BaseModel
from typing import Optional
from models.result import TypeEnum
from datetime import datetime


class ResultInput(BaseModel):
    result: Optional[str] = None
    type: TypeEnum
    input_id: int


class ResultOutput(ResultInput):
    id: int
    created_at: datetime
    updated_at: datetime
