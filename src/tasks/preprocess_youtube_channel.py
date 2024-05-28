from models.input import TypeEnum, Language, TranscriptionType
from schemas.input_schema import InputDataDetails
from sqlalchemy.orm import Session
from logging import getLogger
from services.input_service import InputDataService
from preprocessor.youtube.youtube_channel import YoutubeChannel
from tasks.preprocess import run_preprocess

logger = getLogger(__name__)


def run_youtube_channel_preprocess(
        channel_url: str,
        type_: TypeEnum,
        language: Language,
        transcription_type: TranscriptionType,
        session: Session
) -> None:
    logger.info(f"Preprocessing youtube channel: {channel_url}")

    channel = YoutubeChannel(channel_url)
    channel_videos = channel.get_channel_videos()

    if not channel_videos:
        logger.error(f"No videos found for channel: {channel_url}")
        return

    _service = InputDataService(session)
    for url in channel_videos:
        created_input = _service.create(
            input_data=InputDataDetails(
                type=type_,
                youtube_url=url,
                language=language,
                transcription_type=transcription_type
            )
        )
        run_preprocess(created_input, session)

    return
