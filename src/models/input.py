from enum import Enum

from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy.orm import relationship

from config.database import Base


class TranscriptionType(str, Enum):
    GENERATED = "generated"
    WHISPER_API = "whisper_api"
    WHISPER_LOCAL = "whisper_local"


class Language(str, Enum):
    DANISH = "Danish"
    CZECH = "Czech"
    DUTCH = "Dutch"
    ENGLISH = "English"
    GERMAN = "German"
    ITALIAN = "Italian"
    JAPANESE = "Japanese"
    KOREAN = "Korean"
    POLISH = "Polish"
    SPANISH = "Spanish"
    FRENCH = "French"


class TypeEnum(str, Enum):
    TEXT = "text"
    YOUTUBE = "youtube"
    FILE = "file"
    ARTICLE = "article"
    YOUTUBE_CHANNEL = "channel"
    YOUTUBE_PLAYLIST = "playlist"


class StatusEnum(str, Enum):
    NEW = "new"
    PREPROCESSING = "preprocessing"
    PREPROCESSED = "preprocessed"
    PROCESSING = "processing"
    FAILED = "failed"


class InputData(Base):
    __tablename__ = 'input'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=True)
    type = Column(SQLAlchemyEnum(TypeEnum), nullable=False)
    text = Column(String, nullable=True)
    article_url = Column(String, nullable=True)
    youtube_url = Column(String, nullable=True)
    file_path = Column(String, nullable=True)
    transcription_type = Column(SQLAlchemyEnum(TranscriptionType), nullable=True, default=None)
    language = Column(SQLAlchemyEnum(Language), nullable=True, default=None)
    preprocessed_content = Column(String, nullable=True)
    status = Column(SQLAlchemyEnum(StatusEnum), nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    results = relationship("Result", back_populates="input_data")
