from .preprocess_strategy import PreprocessStrategy
from sqlalchemy.orm import Session
from models.input import StatusEnum
from services.input_service import InputDataService


class TextPreprocessStrategy(PreprocessStrategy):

    def run(self, input_id: int, session: Session) -> None:
        input_service = InputDataService(session)

        input_service.update_status(input_id, StatusEnum.PREPROCESSING)
        print(f"Preprocessing input {input_id}")

        input_object = input_service.get_details(input_id)

        input_service.update_preprocessed_content(input_id, input_object.text)
        input_service.update_status(input_id, StatusEnum.PREPROCESSED)
        input_service.update_title(input_id, input_object[:20])
        print(f"Preprocessed input {input_id}")
