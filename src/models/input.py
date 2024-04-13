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
    PREPROCESSED = "preprocessed"
    PROCESSING = "processing"
    FAILED = "failed"


class InputData(Base):
    __tablename__ = 'input'

    id = Column(Integer, primary_key=True)
    type = Column(SQLAlchemyEnum(TypeEnum), nullable=False)
    text = Column(String, nullable=True)
    article_url = Column(String, nullable=True)
    youtube_url = Column(String, nullable=True)
    file_path = Column(String, nullable=True)
    preprocessed_content = Column(String, nullable=True)
    status = Column(SQLAlchemyEnum(StatusEnum), nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    results = relationship("Result", back_populates="input_data")
