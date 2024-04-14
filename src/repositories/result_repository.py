from models.result import Result
from schemas.result_schema import ResultInput, ResultOutput
from sqlalchemy.orm import Session
from typing import List, Type


class ResultRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, result_data: ResultInput) -> bool:
        result = Result(**result_data.model_dump())
        self.session.add(result)
        self.session.commit()
        return True

    def get_all_by_input_id(self, input_id: int) -> List[ResultOutput]:
        results = self.session.query(Result).filter(Result.input_id == input_id).all()
        return [ResultOutput(**result.__dict__) for result in results]

    def delete(self, result_db: Type[Result]) -> bool:
        self.session.delete(result_db)
        self.session.commit()
        return True

    def get_object(self, result_id: int) -> Type[Result]:
        return self.session.query(Result).filter(Result.id == result_id).first()

    def result_exists(self, result_id: int) -> bool:
        return self.session.query(Result).filter(Result.id == result_id).first() is not None
