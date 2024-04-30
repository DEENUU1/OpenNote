from pydantic import BaseModel
from models.input import TypeEnum, StatusEnum, TranscriptionType
from typing import Optional, List
from datetime import datetime
from .result_schema import ResultOutput


class InputDataInput(BaseModel):
    title: str
    type: TypeEnum
    text: Optional[str] = None
    article_url: Optional[str] = None
    youtube_url: Optional[str] = None
    file_path: Optional[str] = None
    status: StatusEnum = StatusEnum.NEW
    transcription_type: Optional[TranscriptionType] = None


class InputDataOutput(BaseModel):
    title: str
    id: int
    type: TypeEnum
    text: Optional[str] = None
    article_url: Optional[str] = None
    youtube_url: Optional[str] = None
    file_path: Optional[str] = None
    transcription_type: Optional[TranscriptionType] = None
    status: StatusEnum
    created_at: datetime
    updated_at: datetime


class InputDataListOutput(BaseModel):
    prev_page: Optional[int] = None
    next_page: Optional[int] = None
    data: List[Optional[InputDataOutput]]


class InputDataDetails(InputDataOutput):
    preprocessed_content: Optional[str] = None
    results: List[ResultOutput] = []
