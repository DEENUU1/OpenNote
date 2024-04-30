from typing import Optional

from models.input import StatusEnum, TranscriptionType
from services.input_service import InputDataService
from .preprocess_strategy import PreprocessStrategy
from sqlalchemy.orm import Session
from .youtube.youtube_transcription import YoutubeTranscription
from .youtube.youtube_downloader import YoutubeDownloader
from config.settings import settings
from .audio_transcription import AudioTranscription


class YoutubePreprocessStrategy(PreprocessStrategy):

    @staticmethod
    def get_transcription(transcription_type: TranscriptionType, input_object) -> Optional[str]:
        transcription = None

        if transcription_type == TranscriptionType.GENERATED:
            transcription = YoutubeTranscription(input_object.youtube_url).get_youtube_transcription()
            print("Get video transcription from youtube video")

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
                    print("Get video transcription from audio")

        elif transcription_type == TranscriptionType.WHISPER_API:
            pass

        return transcription

    def run(self, input_id: int, session: Session) -> None:
        input_service = InputDataService(session)

        input_service.update_status(input_id, StatusEnum.PREPROCESSING)
        print(f"Preprocessing input {input_id}")

        input_object = input_service.get_details(input_id)
        transcription = self.get_transcription(input_object.transcription_type, input_object)

        if transcription is None:
            input_service.update_status(input_id, StatusEnum.FAILED)
            print(f"Failed to preprocess input {input_id}")
            return

        input_service.update_preprocessed_content(input_id, transcription)
        input_service.update_status(input_id, StatusEnum.PREPROCESSED)

        print(f"Preprocessed input {input_id}")

