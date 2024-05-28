import os

from .preprocess_strategy import PreprocessStrategy
from sqlalchemy.orm import Session
from models.input import StatusEnum
from services.input_service import InputDataService
from .file_parser.factory import FileParserFactory


class FilePreprocessStrategy(PreprocessStrategy):

    @staticmethod
    def get_file_name(file_path: str) -> str:
        try:
            base_name = os.path.basename(file_path)
            file_name, _ = os.path.splitext(base_name)
            return file_name
        except Exception as e:
            print(e)


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
        file_name = self.get_file_name(file_path)
        if file_name:
            input_service.update_title(input_id, file_name)

        print(f"Preprocessed input {input_id}")

