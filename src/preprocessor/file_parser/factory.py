from .parser import Parser
from .pdf import PDFParser
from .txt import TXTParser
from typing import Optional
from .get_file_type import get_file_type


class FileParserFactory:
    @staticmethod
    def get_parser(file_path: str) -> Optional[Parser]:
        file_type = get_file_type(file_path)

        if file_type == ".pdf":
            return PDFParser()
        elif file_type == ".txt":
            return TXTParser()
        else:
            return None
