from pydantic import BaseModel
from typing import Optional


class PreprocessDataInput(BaseModel):
    content: Optional[str] = None
    input_id: int
