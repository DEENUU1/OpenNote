from repositories.result_repository import ResultRepository
from sqlalchemy.orm import Session
from schemas.result_schema import ResultInput
from fastapi.exceptions import HTTPException
from repositories.input_repository import InputDataRepository
from tasks.process import generate_llm_result
from enums.model_enum import ModelEnum


class ResultService:
    def __init__(self, session: Session):
        self.result_repository = ResultRepository(session)
        self.input_data_repository = InputDataRepository(session)

    def create(self, result_data: ResultInput, model_type: ModelEnum) -> bool:
        if not self.input_data_repository.input_object_exists(result_data.input_id):
            raise HTTPException(status_code=404, detail="Input data not found")

        input_data_db = self.input_data_repository.get_object(result_data.input_id)

        llm_result = generate_llm_result(input_data_db, result_data, model_type)

        result_data.result = llm_result
        self.result_repository.create(result_data)
        return True

    def delete_result(self, result_id: int) -> bool:
        if not self.result_repository.result_exists(result_id):
            raise HTTPException(status_code=404, detail="Result not found")

        result_db = self.result_repository.get_object(result_id)

        return self.result_repository.delete(result_db)
