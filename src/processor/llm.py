from typing import Optional, List

import ollama
from groq import Groq
from langchain import OpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from openai import OpenAI

from config.settings import settings
from enums.model_enum import ModelEnum, ModelType
from models.input import Language
from models.result import TypeEnum
from .prompt import get_prompt


class LLMProcess:
    def __init__(
            self,
            model_type: ModelEnum,
            language: Language,
            chunk_size: int = 5000,
            chunk_overlap: int = 200,
    ):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.model_type = model_type
        self.system_message = {"role": "system", "content": f"Response must be in {language.value} language"}

    def get_llm(self) -> Optional[ModelType]:
        if (
                self.model_type == ModelEnum.LLAMA2
                or
                self.model_type == ModelEnum.MISTRAL
        ):
            return ModelType.OLLAMA

        elif (
                self.model_type == ModelEnum.GPT3_5_TURBO
                or
                self.model_type == ModelEnum.GPT4
        ):
            if not settings.OPENAI_APIKEY:
                raise Exception("OpenAI API key is not set")

            return ModelType.OPENAI

        elif (
                self.model_type == ModelEnum.GROQ_GEMMA_7B
                or
                self.model_type == ModelEnum.GROQ_MIXTRAL_8X7B
                or
                self.model_type == ModelEnum.GROQ_LLAMA3_8B
                or
                self.model_type == ModelEnum.GROQ_LLAMA3_70B
        ):
            if not settings.GROQ_APIKEY:
                raise Exception("GROQ API key is not set")

            return ModelType.GROQ

        return None

    def get_llm_response(self, prompt: str) -> Optional[str]:
        llm = self.get_llm()

        if not llm:
            return None

        if llm == ModelType.GROQ:
            groq = Groq(api_key=settings.GROQ_APIKEY)
            groq_result = groq.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    },
                    self.system_message,
                ],
                model=self.model_type.value
            )
            return groq_result.choices[0].message.content

        elif llm == ModelType.OLLAMA:
            ollama_result = ollama.chat(
                model=self.model_type.value,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    },
                    self.system_message,
                ]
            )
            return ollama_result["message"]["content"]

        elif llm == ModelType.OPENAI:
            client = OpenAI(api_key=settings.OPENAI_APIKEY)
            openai_result = client.chat.completions.create(
                messages=[
                    {
                        "user": "user",
                        "content": prompt
                    },
                    self.system_message,
                ],
                model=self.model_type.value
            )
            return openai_result.choices[0].message.content

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
