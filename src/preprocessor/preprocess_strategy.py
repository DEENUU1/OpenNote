from models.input import InputData


class PreprocessStrategy:
    def run(self, input_id: int) -> None:
        pass


class Preprocess:
    def __init__(self, process_strategy: PreprocessStrategy):
        self.process_strategy = process_strategy

    def run(self, input_id: int):
        self.process_strategy.run(input_id)
