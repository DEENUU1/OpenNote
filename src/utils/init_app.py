from models.input import InputData
from config.database import engine
import os


def init_app() -> None:
    # Create db tables
    InputData.metadata.create_all(bind=engine)

    # Create directories
    if not os.path.exists(os.path.join(os.getcwd(), "audio_chunks")):
        os.mkdir(os.path.join(os.getcwd(), "audio_chunks"))

    if not os.path.exists(os.path.join(os.getcwd(), "static")):
        os.mkdir(os.path.join(os.getcwd(), "static"))

    if not os.path.exists(os.path.join(os.getcwd(), "uploads")):
        os.mkdir(os.path.join(os.getcwd(), "uploads"))

    if not os.path.exists(os.path.join(os.getcwd(), "youtube")):
        os.mkdir(os.path.join(os.getcwd(), "youtube"))