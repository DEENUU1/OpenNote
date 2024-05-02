from enum import Enum


class ModelEnum(str, Enum):
    GPT3_5_TURBO = "gpt3.5-turbo"
    GPT4 = "gpt4"
    LLAMA2 = "llama2"
    MISTRAL = "mistral"
    GROQ_LLAMA3_8B = "llama3-8b-8192"
    GROQ_LLAMA3_70B = "llama3-70b-8192"
    GROQ_MIXTRAL_8X7B = "mixtral-8x7b-32768"
    GROQ_GEMMA_7B = "gemma-7b-it"


class ModelType(str, Enum):
    OPENAI = "openai"
    GROQ = "groq"
    OLLAMA = "ollama"
