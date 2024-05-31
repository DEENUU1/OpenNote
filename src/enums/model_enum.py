from enum import Enum


class ModelEnum(str, Enum):
    GPT3_5_TURBO = "gpt-3.5-turbo-0125"
    GPT4 = "gpt-4-32k"
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


def map_tokens_by_model(model: ModelEnum) -> int:
    mapper = {
        "GPT3_5_TURBO": 15000,
        "GPT4": 32000,
        "LLAMA2": 5000,
        "MISTRAL": 5000,
        "GROQ_LLAMA3_8B": 8000,
        "GROQ_LLAMA3_70B": 8000,
        "GROQ_MIXTRAL_8X7B": 31000,
        "GROQ_GEMMA_7B": 8000,
    }
    return mapper[model]
