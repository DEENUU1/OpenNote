from sqlalchemy.orm import Session

from src.schemas.input_schema import InputDataOutput
from src.models.input import TypeEnum
from src.services.input_service import InputDataService
import pytube
from logging import getLogger

logger = getLogger(__name__)


def get_youtube_video_title(url: str) -> str:
    try:
        youtube = pytube.YouTube(url)
        return youtube.title
    except Exception as e:
        logger.error(e)


def get_title_by_source(object_: InputDataOutput, session: Session) -> None:
    _service = InputDataService(session)

    title = ""

    if object_.type == TypeEnum.TEXT:
        title = object_.text[:20]
    elif object_.type == TypeEnum.YOUTUBE:
        title = get_youtube_video_title(object_.youtube_url)
    elif object_.type == TypeEnum.FILE:
        pass
    elif object_.type == TypeEnum.ARTICLE:
        pass
    else:
        return

    _service.update_title(object_.id, title)

