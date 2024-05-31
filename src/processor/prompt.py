from typing import Optional

from models.result import TypeEnum


def get_prompt(type_: TypeEnum, text: str) -> Optional[str]:
    BASIC_PROMPT = "Return only the expected response and nothing else."
    selected_prompt = None

    if type_ == TypeEnum.DETAILED_NOTE:
        selected_prompt = f"""
            Write a detailed note based on the following text: \n
            {text}
        """

    elif type_ == TypeEnum.QUICK_NOTE:
        selected_prompt = f"""
            Write a quick note based on the following text: \n
            {text}
        """

    elif type_ == TypeEnum.DETAILED_SUMMARY:
        selected_prompt = f"""
            Create detailed summary based on the following text: \n
            {text}
        """

    elif type_ == TypeEnum.QUICK_SUMMARY:
        selected_prompt = f"""
            Create quick summary based on the following text: \n
            {text}
        """

    elif type_ == TypeEnum.KEY_TOPICS:
        selected_prompt = f"""
            Create a bullet list of key topics based on the following text: \n
            {text}
        """

    elif type_ == TypeEnum.LIKE_IAM_5:
        selected_prompt = f"""
            Explain me the given text like I am 5 years old child.
            Text: \n
            {text}
        """

    return f"{BASIC_PROMPT}\n\n{selected_prompt}"
