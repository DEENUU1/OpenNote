from sqlalchemy.orm import Session


class PreprocessStrategy:
    def run(self, input_id: int, session: Session) -> None:
        pass


class Preprocess:
    def __init__(self, process_strategy: PreprocessStrategy):
        self.process_strategy = process_strategy

    def run(self, input_id: int, session: Session):
        self.process_strategy.run(input_id, session)
