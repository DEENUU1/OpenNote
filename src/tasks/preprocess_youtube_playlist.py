from models.input import TypeEnum, Language, TranscriptionType
from preprocessor.youtube.youtube_playlist import YoutubePlaylist
from schemas.input_schema import    InputDataInput
from sqlalchemy.orm import Session
from logging import getLogger
from services.input_service import InputDataService
from tasks.preprocess import run_preprocess

logger = getLogger(__name__)


def run_youtube_playlist_preprocess(
        playlist_url: str,
        type_: TypeEnum,
        language: Language,
        transcription_type: TranscriptionType,
        session: Session
) -> None:
    logger.info(f"Preprocessing youtube playlist: {playlist_url}")

    channel = YoutubePlaylist(playlist_url)
    playlist_videos = channel.get_playlist_videos()

    if not playlist_videos:
        logger.error(f"No videos found for playlist: {playlist_url}")
        return

    _service = InputDataService(session)
    for url in playlist_videos:
        created_input = _service.create(
            input_data=InputDataInput(
                type=type_,
                youtube_url=url,
                language=language,
                transcription_type=transcription_type
            )
        )
        run_preprocess(created_input, session)

    return
