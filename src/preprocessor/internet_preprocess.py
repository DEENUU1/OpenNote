from .preprocess_strategy import PreprocessStrategy
from sqlalchemy.orm import Session
from models.input import StatusEnum
from services.input_service import InputDataService
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.webdriver import WebDriver
from webdriver_manager.chrome import ChromeDriverManager
from typing import Optional
from bs4 import BeautifulSoup


class InternetPreprocessStrategy(PreprocessStrategy):

    @staticmethod
    def get_driver() -> WebDriver:
        return webdriver.Chrome(
            service=ChromeService(
                ChromeDriverManager().install()
            )
        )

    def get_page_content(self, url: str) -> Optional[str]:
        driver = self.get_driver()
        try:
            driver.get(url)
        except Exception as e:
            print(e)
            return None

        return driver.page_source

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
        print(f"Preprocessing input {input_id}")

        input_object = input_service.get_details(input_id)

        page_content = self.get_page_content(input_object.article_url)
        parsed_content = self.parse_page(page_content)

        input_service.update_preprocessed_content(input_id, parsed_content)

        input_service.update_status(input_id, StatusEnum.PREPROCESSED)

        print(f"Preprocessed input {input_id}")
