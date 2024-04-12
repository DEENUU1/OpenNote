from pydantic import BaseModel
from models.input import TypeEnum, StatusEnum
from typing import Optional, List
from datetime import datetime


class InputDataInput(BaseModel):
    type: TypeEnum
    text: Optional[str] = None
    article_url: Optional[str] = None
    youtube_url: Optional[str] = None
    file_path: Optional[str] = None
    status: StatusEnum = StatusEnum.NEW


class InputDataOutput(BaseModel):
    id: int
    type: TypeEnum
    text: Optional[str] = None
    article_url: Optional[str] = None
    youtube_url: Optional[str] = None
    file_path: Optional[str] = None
    status: StatusEnum
    created_at: datetime
    updated_at: Optional[datetime] = None


class InputDataListOutput(BaseModel):
    prev_page: Optional[int]
    next_page: Optional[int]
    data: List[Optional[InputDataOutput]]

