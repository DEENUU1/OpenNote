from typing import Optional, Union, List

from groq import Groq
from langchain import OpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.llms import Ollama
from langchain_core.documents import Document
from langchain_core.prompts import PromptTemplate

from config.settings import settings
from enums.model_enum import ModelEnum
from models.result import TypeEnum
from .prompt import get_prompt
from langchain_groq import ChatGroq


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

    def get_llm(self) -> Optional[Union[Ollama, Groq]]:
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

        elif (
                self.model_type == ModelEnum.GROQ_LLAMA_3_70_B
                or
                self.model_type == ModelEnum.GROQ_GEMMA
                or
                self.model_type == ModelEnum.GROQ_MIXTRAL
        ):
            if not settings.GROQ_APIKEY:
                raise Exception("GROQ API key is not set")

            return Groq(api_key=settings.GROQ_APIKEY)

        return None

    def get_llm_response(self, prompt: str) -> Optional[str]:
        llm = self.get_llm()

        if not llm:
            return None

        if isinstance(llm, Groq):
            groq_result = llm.chat.completions.create(
                messages=[{
                    "role": "user",
                    "content": prompt
                }],
                model=self.model_type.value
            )
            return groq_result.choices[0].message.content

    def split_text_to_chunks(self, text: str) -> List[Document]:
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap)

        split_text = text_splitter.create_documents([text])
        return split_text

    def process(self, input_data: str, result_type: TypeEnum) -> Optional[str]:
        documents = self.split_text_to_chunks(input_data)

        processed_text = ""
        for document in documents:
            prompt = get_prompt(result_type, document.page_content)
            llm_response = self.get_llm_response(prompt)
            processed_text += llm_response + "\n\n"

        return processed_text
