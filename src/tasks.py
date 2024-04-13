from config.database import get_db
from preprocessor.preprocess_strategy import Preprocess
from preprocessor.text_preprocess import TextPreprocessStrategy
from preprocessor.internet_preprocess import InternetPreprocessStrategy
from preprocessor.youtube_preprocess import YoutubePreprocessStrategy
from preprocessor.file_preprocess import FilePreprocessStrategy


def run_preprocess():
    text_preprocessing = TextPreprocessStrategy()
    internet_preprocessing = InternetPreprocessStrategy()
    youtube_preprocessing = YoutubePreprocessStrategy()
    file_preprocessing = FilePreprocessStrategy()

    preprocess = Preprocess(file_preprocessing)
    preprocess.run(12, next(get_db()))



if __name__ == "__main__":
    run_preprocess()
