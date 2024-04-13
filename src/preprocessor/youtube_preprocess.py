from models.input import StatusEnum
from services.input_service import InputDataService
from .preprocess_strategy import PreprocessStrategy
from sqlalchemy.orm import Session
from .youtube_transcription.youtube_transcription import YoutubeTranscription


class YoutubePreprocessStrategy(PreprocessStrategy):


    def run(self, input_id: int, session: Session) -> None:
        input_service = InputDataService(session)

        # input_service.update_status(input_id, StatusEnum.PREPROCESSING)
        print(f"Preprocessing input {input_id}")

        # input_object = input_service.get_details(input_id)
        transcription = None
        youtube_transcription = YoutubeTranscription("https://www.youtube.com/watch?v=44HSTVBvAO4").get_youtube_transcription()
        if youtube_transcription:
            transcription = youtube_transcription
            print(transcription)
        else:
            pass

        if transcription is None:
            input_service.update_status(input_id, StatusEnum.FAILED)
            print(f"Failed to preprocess input {input_id}")
            return

        # input_service.update_preprocessed_content(input_id, input_object.text)

        # input_service.update_status(input_id, StatusEnum.PREPROCESSED)

        print(f"Preprocessed input {input_id}")

