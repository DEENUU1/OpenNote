from typing import Optional

from langchain_community.document_loaders import PyPDFLoader

from .parser import Parser


class PDFParser(Parser):

    def parse(self, file_path: str) -> Optional[str]:
        pages = None
        try:
            loader = PyPDFLoader("uploads/book.pdf")
            pages = loader.load_and_split()

        except Exception as e:
            print(e)
            return None

        if pages is None:
            return None

        content = ""
        for page in pages:
            content += page.page_content + "\n"

        return content
