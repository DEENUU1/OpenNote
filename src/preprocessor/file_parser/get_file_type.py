import pathlib
from typing import Optional


def get_file_type(file_path: str) -> Optional[str]:
    file_path = pathlib.Path(file_path)
    return file_path.suffix
