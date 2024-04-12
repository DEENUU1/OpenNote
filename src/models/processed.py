from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from config.database import Base


class ProcessedData(Base):
    __tablename__ = 'processed_data'

    id = Column(Integer, primary_key=True)
    content = Column(String)
    input_id = Column(Integer, ForeignKey('input.id'))

    input = relationship("Input", back_populates="processed_data")
