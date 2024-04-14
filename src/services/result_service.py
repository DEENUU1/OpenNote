from repositories.result_repository import ResultRepository
from sqlalchemy.orm import Session
from schemas.result_schema import ResultInput
from fastapi.exceptions import HTTPException
from repositories.input_repository import InputDataRepository
from processor.llm import LLMProcess


class ResultService:
    def __init__(self, session: Session):
        self.result_repository = ResultRepository(session)
        self.input_data_repository = InputDataRepository(session)

    def create(self, result_data: ResultInput) -> bool:
        if not self.input_data_repository.input_object_exists(result_data.input_id):
            raise HTTPException(status_code=404, detail="Input data not found")

        input_data_db = self.input_data_repository.get_object(result_data.input_id)

        llm_process = LLMProcess()
        llm_result = llm_process.process(input_data_db.preprocessed_content, result_data.type)

        result_data.result = llm_result
        self.result_repository.create(result_data)
        return True

    def delete_result(self, result_id: int) -> bool:
        if not self.result_repository.result_exists(result_id):
            raise HTTPException(status_code=404, detail="Result not found")

        result_db = self.result_repository.get_object(result_id)

        return self.result_repository.delete(result_db)
