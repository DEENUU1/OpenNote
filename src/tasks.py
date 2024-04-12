from config.database import get_db
from preprocessor.preprocess_strategy import Preprocess
from preprocessor.text_preprocess import TextPreprocessStrategy
from preprocessor.internet_preprocess import InternetPreprocessStrategy


def run_preprocess():
    text_preprocessing = TextPreprocessStrategy()
    internet_preprocessing = InternetPreprocessStrategy()

    preprocess = Preprocess(internet_preprocessing)
    preprocess.run(2, next(get_db()))
    preprocess.run(3, next(get_db()))
    preprocess.run(4, next(get_db()))
    preprocess.run(5, next(get_db()))
    preprocess.run(6, next(get_db()))
    preprocess.run(7, next(get_db()))
    preprocess.run(8, next(get_db()))
    preprocess.run(9, next(get_db()))


if __name__ == "__main__":
    run_preprocess()
