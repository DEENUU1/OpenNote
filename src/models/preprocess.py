from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from config.database import Base


class PreprocessData(Base):
    __tablename__ = 'preprocess_data'

    id = Column(Integer, primary_key=True)
    content = Column(String)
    input_id = Column(Integer, ForeignKey('input.id'))

    input = relationship("InputData", back_populates="preprocess_data")
