from typing import List

from repositories.result_repository import ResultRepository
from sqlalchemy.orm import Session
from schemas.result_schema import ResultInput, ResultOutput
from fastapi.exceptions import HTTPException


class ResultService:
    def __init__(self, session: Session):
        self.result_repository = ResultRepository(session)

    def create(self, result_data: ResultInput) -> bool:
        return self.result_repository.create(result_data)

    def get_all(self) -> List[ResultOutput]:
        return self.result_repository.get_all()

    def delete_result(self, result_id: int) -> bool:
        if not self.result_repository.result_exists(result_id):
            raise HTTPException(status_code=404, detail="Result not found")

        result_db = self.result_repository.get_object(result_id)

        self.result_repository.delete(result_db)
