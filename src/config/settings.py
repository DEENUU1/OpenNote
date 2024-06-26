import os
from typing import Optional, Final

from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from fastapi.templating import Jinja2Templates

load_dotenv()


class Settings(BaseSettings):
    """
    Application settings.
    """
    # Debug mode is set by default to True because it's local application
    DEBUG: bool = True
    # Title is the name of application
    TITLE: str = "OpenNote"
    # SQLITE connection string
    SQLITE_CONNECTION_STRING: Optional[str] = "sqlite:///database.db"
    # Templates
    TEMPLATES: Jinja2Templates = Jinja2Templates(directory="templates")
    # File path uploaded to process
    UPLOAD_FILE_PATH: Final[str] = "uploads/"
    # File path for downloaded Youtube video
    YOUTUBE_FILE_PATH: Final[str] = "youtube/"
    # File path audio chunks
    AUDIO_CHUNK_FILE_PATH: Final[str] = "audio_chunks/"
    # Whisper model
    WHISPER_MODEL: str = os.getenv("WHISPER_MODEL")
    # tiny, base, small, medium, large
    # for more details about models check https://github.com/openai/whisper
    LLM_MODEL: Optional[str] = os.getenv("LLM_MODEL")
    # LLMs
    OPENAI_APIKEY: Optional[str] = os.getenv("OPENAI_APIKEY", None)
    GROQ_APIKEY: Optional[str] = os.getenv("GROQ_APIKEY", None)


settings = Settings()
