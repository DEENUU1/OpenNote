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
    updated_at: datetime


class InputDataListOutput(BaseModel):
    prev_page: Optional[int] = None
    next_page: Optional[int] = None
    data: List[Optional[InputDataOutput]]


class InputDataDetails(InputDataOutput):
    preprocessed_content: Optional[str] = None
    processed_content: Optional[str] = None

