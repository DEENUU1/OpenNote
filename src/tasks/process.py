from typing import Optional
from processor.llm import LLMProcess


def generate_llm_result(input_data_db, result_data) -> Optional[str]:
    llm_process = LLMProcess()
    llm_result = llm_process.process(input_data_db.preprocessed_content, result_data.type)
    return llm_result
