from typing import Optional

from langchain_community.document_loaders import PyPDFLoader

from .parser import Parser
from logging import getLogger

logger = getLogger(__name__)


class PDFParser(Parser):

    def parse(self, file_path: str) -> Optional[str]:
        try:
            logger.info("Loading PDF file...")
            loader = PyPDFLoader("uploads/book.pdf")
            pages = loader.load_and_split()

        except Exception as e:
            logger.error(f"Error loading PDF file: {e}")
            return None

        if pages is None:
            logger.error("No pages found in PDF file")
            return None

        content = ""
        for page in pages:
            content += page.page_content + "\n"

        logger.info("PDF file loaded successfully")
        return content
