from models.result import Result
from schemas.result_schema import ResultInput, ResultOutput
from sqlalchemy.orm import Session


class ResultRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, result_data: ResultInput) -> bool:
        result = Result(**result_data.dict())
        self.session.add(result)
        self.session.commit()
        return True

    def get_all(self) -> ResultOutput:
        results = self.session.query(Result).all()
        return ResultOutput(results=[result.__dict__ for result in results])

    def delete(self, result_id: int) -> bool:
        result = self.session.query(Result).filter(Result.id == result_id).first()
        self.session.delete(result)
        self.session.commit()
        return True
