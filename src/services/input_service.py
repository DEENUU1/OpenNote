from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from repositories.input_repository import InputDataRepository
from schemas.input_schema import InputDataListOutput, InputDataDetails, InputDataOutput
from repositories.result_repository import ResultRepository


class InputDataService:
    def __init__(self, session: Session):
        self.input_repository = InputDataRepository(session)
        self.result_repository = ResultRepository(session)

    def create(self, input_data) -> InputDataOutput:
        return self.input_repository.create(input_data)

    def delete(self, input_id: int) -> bool:
        if not self.input_repository.input_object_exists(input_id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Input not found")

        input_object = self.input_repository.get_object(input_id)

        return self.input_repository.delete(input_object)

    def update_title(self, input_id: int, title: str) -> bool:
        if not self.input_repository.input_object_exists(input_id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Input not found")

        input_object = self.input_repository.get_object(input_id)

        return self.input_repository.update_title(input_object, title)

    def get_all(self, page: int = 1, page_limit: int = 50) -> InputDataListOutput:
        return self.input_repository.get_all(page, page_limit)

    def get_details(self, input_id: int) -> InputDataDetails:
        if not self.input_repository.input_object_exists(input_id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Input not found")

        result_list = self.result_repository.get_all_by_input_id(input_id)
        input_details = self.input_repository.get_details(input_id)
        input_details.results = result_list
        return input_details

    def update_status(self, input_id: int, new_status: str) -> bool:
        if not self.input_repository.input_object_exists(input_id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Input not found")

        input_object = self.input_repository.get_object(input_id)

        return self.input_repository.update_status(input_object, new_status)

    def update_preprocessed_content(self, input_id: int, new_content: str) -> bool:
        if not self.input_repository.input_object_exists(input_id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Input not found")

        input_object = self.input_repository.get_object(input_id)

        return self.input_repository.update_preprocessed_content(input_object, new_content)

    def update_processed_content(self, input_id: int, new_content: str) -> bool:
        if not self.input_repository.input_object_exists(input_id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Input not found")

        input_object = self.input_repository.get_object(input_id)

        return self.input_repository.update_processed_content(input_object, new_content)
