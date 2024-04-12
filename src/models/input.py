from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.orm import relationship
from config.database import Base
from sqlalchemy import Enum as SQLAlchemyEnum
from enum import Enum


class TypeEnum(str, Enum):
    TEXT = "text"
    YOUTUBE = "youtube"
    FILE = "file"
    ARTICLE = "article"


class StatusEnum(str, Enum):
    NEW = "new"
    PREPROCESSING = "preprocessing"
    PROCESSING = "processing"
    FAILED = "failed"
    DONE = "done"


class InputData(Base):
    __tablename__ = 'input'

    id = Column(Integer, primary_key=True)
    type = Column(SQLAlchemyEnum(TypeEnum), nullable=False)
    input_string = Column(String)
    article_url = Column(String)
    youtube_url = Column(String)
    file_path = Column(String)
    status = Column(SQLAlchemyEnum(StatusEnum), nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    preprocess_data = relationship("PreprocessData", uselist=False, back_populates="input")
    processed_data = relationship("ProcessedData", uselist=False, back_populates="input")
