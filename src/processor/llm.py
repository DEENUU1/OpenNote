from langchain_core.documents import Document
from langchain_core.prompts import PromptTemplate

from config.settings import settings
from langchain_community.llms import Ollama
from typing import Optional, List
from langchain.text_splitter import CharacterTextSplitter
from models.result import TypeEnum
from .prompt import get_prompt


class LLMProcess:
    def __init__(self, chunk_size: int = 2000, chunk_overlap: int = 200):
        self.llm = Ollama(model=settings.LLM_MODEL)
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def get_llm_response(self, input_data: str, prompt: PromptTemplate) -> Optional[str]:
        prompt_model = prompt | self.llm
        output = prompt_model.invoke({"text": input_data})
        return output

    def split_text_to_chunks(self, text: str) -> List[Document]:
        text_splitter = CharacterTextSplitter(chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap)

        split_text = text_splitter.create_documents([text])
        return split_text

    def process(self, input_data: str, result_type: TypeEnum) -> Optional[str]:
        documents = self.split_text_to_chunks(input_data)

        processed_text = ""
        for document in documents:
            prompt = get_prompt(result_type)
            llm_response = self.get_llm_response(document.page_content, prompt)
            processed_text += llm_response + "\n\n"

        return processed_text
