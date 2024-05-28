from typing import Union
from preprocessor.preprocess_strategy import Preprocess
from preprocessor.text_preprocess import TextPreprocessStrategy
from preprocessor.internet_preprocess import InternetPreprocessStrategy
from preprocessor.youtube_preprocess import YoutubePreprocessStrategy
from preprocessor.file_preprocess import FilePreprocessStrategy
from models.input import TypeEnum
from schemas.input_schema import InputDataDetails, InputDataOutput
from sqlalchemy.orm import Session


def run_preprocess(input_details: Union[InputDataDetails, InputDataOutput], session: Session) -> None:
    print(f"Run preprocess tasks for: {input_details.id} input")

    preprocessor_map = {
        TypeEnum.TEXT:  TextPreprocessStrategy,
        TypeEnum.YOUTUBE: YoutubePreprocessStrategy,
        TypeEnum.FILE: FilePreprocessStrategy,
        TypeEnum.ARTICLE: InternetPreprocessStrategy
    }

    preprocessor = preprocessor_map[input_details.type]
    print(f"Preprocess strategy: {preprocessor}")

    preprocess = Preprocess(preprocessor())
    preprocess.run(input_details.id, session)
    print(f"Preprocess done for: {input_details.id} input")
