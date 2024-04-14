from typing import Optional

from langchain.prompts import PromptTemplate
from models.result import TypeEnum


note_prompt = PromptTemplate(
    template="Based on the text provided, create a detailed note. \n{text}",
    input_variables=["text"]
)

summary_prompt = PromptTemplate(
    template="Based on the text provided, create detailed a summary. \n{text}",
    input_variables=["text"]
)


def get_prompt(type: TypeEnum) -> Optional[PromptTemplate]:
    if type == TypeEnum.NOTE:
        return note_prompt
    elif type == TypeEnum.SUMMARY:
        return summary_prompt

    return None
