from .preprocess_strategy import PreprocessStrategy
from sqlalchemy.orm import Session
from models.input import StatusEnum
from services.input_service import InputDataService
from .file_parser.factory import FileParserFactory


class FilePreprocessStrategy(PreprocessStrategy):

    def run(self, input_id: int, session: Session) -> None:
        input_service = InputDataService(session)

        input_service.update_status(input_id, StatusEnum.PREPROCESSING)
        print(f"Preprocessing input {input_id}")

        input_object = input_service.get_details(input_id)

        file_path = input_object.file_path
        file_parser_factory = FileParserFactory().get_parser(file_path)

        if not file_parser_factory:
            input_service.update_status(input_id, StatusEnum.FAILED)
            print(f"Failed preprocessing input {input_id}")
            return

        file_content = file_parser_factory.parse(file_path)

        input_service.update_preprocessed_content(input_id, file_content)

        input_service.update_status(input_id, StatusEnum.PREPROCESSED)

        print(f"Preprocessed input {input_id}")

