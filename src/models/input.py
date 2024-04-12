from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from config.database import Base


class Input(Base):
    __tablename__ = 'input'

    id = Column(Integer, primary_key=True)
    type = Column(String)
    input_string = Column(String)
    article_url = Column(String)
    youtube_url = Column(String)
    file_path = Column(String)
    status = Column(String)

    preprocess_data = relationship("PreprocessData", uselist=False, back_populates="input")
    processed_data = relationship("ProcessedData", uselist=False, back_populates="input")
