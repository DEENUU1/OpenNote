from langchain_core.documents import Document
from langchain_core.prompts import PromptTemplate

from langchain_community.llms import Ollama
from langchain.text_splitter import RecursiveCharacterTextSplitter
from models.result import TypeEnum
from .prompt import get_prompt
from enums.model_enum import ModelEnum
from typing import Optional, Union, List
from config.settings import settings
from langchain import OpenAI


class LLMProcess:
    def __init__(
            self,
            model_type: ModelEnum,
            chunk_size: int = 5000,
            chunk_overlap: int = 200,
    ):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.model_type = model_type

    def get_llm(self) -> Optional[Union[Ollama, str]]:
        if (
                self.model_type == ModelEnum.LLAMA2
                or
                self.model_type == ModelEnum.MISTRAL
        ):
            return Ollama(model=settings.LLM_MODEL)

        elif (
                self.model_type == ModelEnum.GPT3_5_TURBO
                or
                self.model_type == ModelEnum.GPT4
        ):
            if not settings.OPENAI_APIKEY:
                raise Exception("OpenAI API key is not set")

            return OpenAI(openai_api_key=settings.OPENAI_APIKEY, model_name=self.model_type)

        return None

    def get_llm_response(self, input_data: str, prompt: PromptTemplate) -> Optional[str]:
        llm = self.get_llm()
        prompt_model = prompt | llm
        output = prompt_model.invoke({"text": input_data})
        return output

    def split_text_to_chunks(self, text: str) -> List[Document]:
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap)

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
