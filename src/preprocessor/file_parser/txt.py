from typing import Optional
from .parser import Parser
from logging import getLogger

logger = getLogger(__name__)


class TXTParser(Parser):

    def parse(self, file_path: str) -> Optional[str]:
        try:
            logger.info(f"Parsing {file_path}")
            with open(file_path, 'r') as file:
                return file.read()
        except Exception as e:
            logger.error(f"Error parsing {file_path}")
            return None
