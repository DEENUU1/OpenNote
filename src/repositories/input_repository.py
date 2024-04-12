from sqlalchemy.orm import Session
from typing import List, Optional, Type
from schemas.input_schema import InputDataListOutput, InputDataOutput, InputDataInput
from models.input import InputData
from sqlalchemy import func, desc


class InputDataRepository:

    def __init__(self, session: Session):
        self.session: Session = session

    def create(self, input_data: InputDataInput) -> bool:
        db_input = InputData(**input_data.model_dump())
        self.session.add(db_input)
        self.session.commit()
        self.session.refresh(db_input)
        return True

    def delete(self, input_object: Type[InputDataInput]) -> bool:
        self.session.delete(input_object)
        self.session.commit()
        return True

    def get_object(self, input_id: int) -> Type[InputData]:
        return self.session.query(InputData).filter(InputData.id == input_id).first()

    def get_details(self, input_id: int) -> InputDataOutput:
        return InputDataOutput(**self.get_object(input_id).model_dump())

    def update_status(self, input_object: Type[InputData], status: str) -> bool:
        input_object.status = status
        self.session.commit()
        return True

    def input_object_exists(self, input_id: int) -> bool:
        return self.session.query(InputData).filter(InputData.id == input_id).first() is not None

    def get_all(self, page: int = 1, page_limit: int = 50) -> InputDataListOutput:
        total_input_query = self.session.query(func.count(InputData.id))

        inputs = self.session.query(InputData)

        # Sort from oldest to newest
        inputs = inputs.order_by(desc(InputData.created_at))

        total_offers = total_input_query.scalar()

        total_pages = (total_offers + page_limit - 1) // page_limit
        prev_page = max(page - 1, 1) if page > 1 else None
        next_page = min(page + 1, total_pages) if page < total_pages else None

        offset = (page - 1) * page_limit if page > 0 else 0
        inputs = inputs.offset(offset).limit(page_limit).all()

        input_list = [InputDataOutput(**item.__dict__) for item in inputs]

        return InputDataListOutput(
            data=input_list,
            prev_page=prev_page,
            next_page=next_page,
        )
