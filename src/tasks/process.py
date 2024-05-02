from typing import Optional
from processor.llm import LLMProcess
from enums.model_enum import ModelEnum


def generate_llm_result(input_data_db, result_data, model_type: ModelEnum) -> Optional[str]:
    llm_process = LLMProcess(model_type, input_data_db.language)
    llm_result = llm_process.process(input_data_db.preprocessed_content, result_data.type)
    return llm_result
