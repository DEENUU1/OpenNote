from langchain_community.llms import Ollama
from sqlalchemy.orm import Session
from schemas.input_schema import InputDataDetails
from processor.llm import LLMProcess
from models.result import TypeEnum


def generate_result(input_details: InputDataDetails, session: Session) -> None:
    print(f"Run process tasks for: {input_details.id} input")
    # processed_data = input_details.processed_data

    llm_process = LLMProcess()
    result = llm_process.process()

