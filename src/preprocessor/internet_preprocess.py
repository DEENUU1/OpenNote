from .preprocess_strategy import PreprocessStrategy
from sqlalchemy.orm import Session
from models.input import StatusEnum
from services.input_service import InputDataService
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.webdriver import WebDriver
from webdriver_manager.chrome import ChromeDriverManager
from typing import Optional, Tuple
from bs4 import BeautifulSoup
from logging import getLogger

logger = getLogger(__name__)


class InternetPreprocessStrategy(PreprocessStrategy):

    @staticmethod
    def get_driver() -> WebDriver:
        return webdriver.Chrome(
            service=ChromeService(
                ChromeDriverManager().install()
            )
        )

    def get_page_content_and_title(self, url: str) -> Tuple[Optional[str], Optional[str]]:
        driver = self.get_driver()
        try:
            driver.get(url)
        except Exception as e:
            logger.error(f"Error while fetching page: {e}")
            return None, None

        return driver.page_source, driver.title

    @staticmethod
    def parse_page(page_source: str) -> Optional[str]:
        soup = BeautifulSoup(page_source, "html.parser")

        tags = ["h1", "h2", "h3", "h4", "h5", "p"]

        text = ""
        for tag in tags:
            tag_contents = soup.find_all(tag)
            for tag_content in tag_contents:
                text += tag_content.text + " "

        return text

    def run(self, input_id: int, session: Session) -> None:
        input_service = InputDataService(session)

        input_service.update_status(input_id, StatusEnum.PREPROCESSING)
        logger.info(f"Preprocessing input {input_id}")

        input_object = input_service.get_details(input_id)

        page_content, title = self.get_page_content_and_title(input_object.article_url)
        parsed_content = self.parse_page(page_content)

        input_service.update_preprocessed_content(input_id, parsed_content)
        input_service.update_status(input_id, StatusEnum.PREPROCESSED)
        input_service.update_title(input_id, title)

        logger.info(f"Preprocessed input {input_id}")

