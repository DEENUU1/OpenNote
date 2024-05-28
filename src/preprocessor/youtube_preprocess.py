from typing import Optional

from models.input import StatusEnum, TranscriptionType
from services.input_service import InputDataService
from .preprocess_strategy import PreprocessStrategy
from sqlalchemy.orm import Session
from .youtube.youtube_transcription import YoutubeTranscription
from .youtube.youtube_downloader import YoutubeDownloader
from config.settings import settings
from .audio_transcription import AudioTranscription
import pytube
from logging import getLogger

logger = getLogger(__name__)


class YoutubePreprocessStrategy(PreprocessStrategy):

    @staticmethod
    def get_youtube_video_title(url: str) -> str:
        try:
            youtube = pytube.YouTube(url)
            return youtube.title
        except Exception as e:
            logger.error(f"Error getting video title: {e}")

    @staticmethod
    def get_transcription(transcription_type: TranscriptionType, input_object) -> Optional[str]:
        transcription = None

        if transcription_type == TranscriptionType.GENERATED:
            transcription = YoutubeTranscription(
                input_object.youtube_url,
                input_object.language
            ).get_youtube_transcription()
            logger.info(f"Get video transcription from youtube: {transcription}")

        elif transcription_type == TranscriptionType.WHISPER_LOCAL:
            youtube_downloader = YoutubeDownloader(input_object.youtube_url).download()
            if youtube_downloader:
                audio_transcription = AudioTranscription(
                    audio_file_path=youtube_downloader,
                    whisper_model=settings.WHISPER_MODEL,
                    chunk_size=150
                ).run()

                if audio_transcription:
                    transcription = audio_transcription
                    logger.info(f"Get video transcription from audio: {transcription}")

        elif transcription_type == TranscriptionType.WHISPER_API:
            pass

        return transcription

    def run(self, input_id: int, session: Session) -> None:
        input_service = InputDataService(session)

        input_service.update_status(input_id, StatusEnum.PREPROCESSING)
        logger.info(f"Preprocessing input {input_id}")

        input_object = input_service.get_details(input_id)
        transcription = self.get_transcription(input_object.transcription_type, input_object)

        if transcription is None:
            input_service.update_status(input_id, StatusEnum.FAILED)
            logger.info(f"Failed preprocessing input {input_id}")
            return

        input_service.update_preprocessed_content(input_id, transcription)
        input_service.update_status(input_id, StatusEnum.PREPROCESSED)
        video_title = self.get_youtube_video_title(input_object.youtube_url)
        if video_title:
            input_service.update_title(input_id, video_title)
        logger.info(f"Preprocessed input {input_id}")
