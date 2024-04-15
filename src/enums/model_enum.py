from enum import Enum


class ModelEnum(str, Enum):
    GPT3_5_TURBO = "gpt3.5-turbo"
    GPT4 = "gpt4"
    LLAMA2 = "llama2"
    MISTRAL = "mistral"
