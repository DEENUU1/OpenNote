from typing import Optional


from .parser import Parser


class TXTParser(Parser):

    def parse(self, file_path: str) -> Optional[str]:
        try:
            with open(file_path, 'r') as file:
                return file.read()
        except Exception as e:
            print(e)
            return None

