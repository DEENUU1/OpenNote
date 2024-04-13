from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship

from config.database import Base
from sqlalchemy import Enum as SQLAlchemyEnum
from enum import Enum


class TypeEnum(str, Enum):
    NOTE = "note"
    SUMMARY = "summary"


class Result(Base):
    __tablename__ = 'result'

    id = Column(Integer, primary_key=True)
    result = Column(String, nullable=True)
    type = Column(SQLAlchemyEnum(TypeEnum), nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    input_id = Column(Integer, ForeignKey('input.id'))

    input_data = relationship("InputData", back_populates="results")
