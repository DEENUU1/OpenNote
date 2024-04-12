from config.settings import settings
from fastapi import HTTPException
from typing import Optional


def upload_file(file) -> Optional[str]:
    file_path = None

    if file and file.filename:

        if not file.filename.endswith((".txt", ".pdf")):
            raise HTTPException(status_code=400, detail="Invalid file type")

        file_path = f"{settings.UPLOAD_FILE_PATH}{file.filename}"
        with open(file_path, "wb") as f:
            f.write(file.file.read())

    return file_path
