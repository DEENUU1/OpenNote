from models.input import StatusEnum
from services.input_service import InputDataService
from .preprocess_strategy import PreprocessStrategy
from sqlalchemy.orm import Session
from .youtube.youtube_transcription import YoutubeTranscription
from .youtube.youtube_downloader import YoutubeDownloader
from config.settings import settings
from .audio_transcription import AudioTranscription


class YoutubePreprocessStrategy(PreprocessStrategy):

    def run(self, input_id: int, session: Session) -> None:
        input_service = InputDataService(session)

        input_service.update_status(input_id, StatusEnum.PREPROCESSING)
        print(f"Preprocessing input {input_id}")

        input_object = input_service.get_details(input_id)
        transcription = None
        youtube_transcription = YoutubeTranscription(input_object.youtube_url).get_youtube_transcription()
        if youtube_transcription:
            transcription = youtube_transcription
            print("Get video transcription from youtube video")

        else:
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

        if transcription is None:
            input_service.update_status(input_id, StatusEnum.FAILED)
            print(f"Failed to preprocess input {input_id}")
            return

        input_service.update_preprocessed_content(input_id, transcription)

        input_service.update_status(input_id, StatusEnum.PREPROCESSED)

        print(f"Preprocessed input {input_id}")

