from typing import Optional

from models.result import TypeEnum


def get_prompt(type_: TypeEnum, text: str) -> Optional[str]:
    if type_ == TypeEnum.DETAILED_NOTE:
        return f"""
            Write a detailed note based on the following text: \n
            {text}
        """

    elif type_ == TypeEnum.QUICK_NOTE:
        return f"""
            Write a quick note based on the following text: \n
            {text}
        """

    elif type_ == TypeEnum.DETAILED_SUMMARY:
        return f"""
            Create detailed summary based on the following text: \n
            {text}
        """

    elif type_ == TypeEnum.QUICK_SUMMARY:
        return f"""
            Create quick summary based on the following text: \n
            {text}
        """

    elif type_ == TypeEnum.KEY_TOPICS:
        return f"""
            Create a bullet list of key topics based on the following text: \n
            {text}
        """

    elif type_ == TypeEnum.LIKE_IAM_5:
        return f"""
            Explain me the given text like I am 5 years old child.
            Text: \n
            {text}
        """

    return None