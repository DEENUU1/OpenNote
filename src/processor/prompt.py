from typing import Optional

from models.result import TypeEnum


def get_prompt(type_: TypeEnum, text: str) -> Optional[str]:
    if type_ == TypeEnum.NOTE:
        return f"Based on the given text, create a detailed note. \n{text}"

    elif type_ == TypeEnum.SUMMARY:
        return f"Based on the given text, create detailed summary. \n{text}"

    return None
