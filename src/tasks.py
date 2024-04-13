from config.database import get_db
from preprocessor.preprocess_strategy import Preprocess
from preprocessor.text_preprocess import TextPreprocessStrategy
from preprocessor.internet_preprocess import InternetPreprocessStrategy
from preprocessor.youtube_preprocess import YoutubePreprocessStrategy


def run_preprocess():
    text_preprocessing = TextPreprocessStrategy()
    internet_preprocessing = InternetPreprocessStrategy()
    youtube_preprocessing = YoutubePreprocessStrategy()

    preprocess = Preprocess(youtube_preprocessing)
    preprocess.run(2, next(get_db()))



if __name__ == "__main__":
    run_preprocess()
