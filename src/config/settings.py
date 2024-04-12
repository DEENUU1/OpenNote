import os
from typing import Optional

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
    TITLE: Optional[str] = os.getenv("TITLE")
    # SQLITE connection string
    SQLITE_CONNECTION_STRING: Optional[str] = "sqlite:///database.db"
    # Templates
    TEMPLATES: Jinja2Templates = Jinja2Templates(directory="templates")
    # File path uploaded to process
    UPLOAD_FILE_PATH = "uploads/"


settings = Settings()
