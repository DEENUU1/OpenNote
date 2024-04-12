from fastapi import Request, APIRouter, Depends, Form, File, UploadFile, HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from starlette import status

from config.database import get_db
from config.settings import settings
from schemas.input_schema import InputDataInput
from services.input_service import InputDataService
from models.input import TypeEnum
from typing import Optional
from fastapi.responses import RedirectResponse


router = APIRouter(
    prefix="",
    tags=["Home"],
)


@router.post("/input", status_code=201)
def create_input_data(
        type: TypeEnum = Form(...),
        text: Optional[str] = Form(None),
        article_url: Optional[str] = Form(None),
        youtube_url: Optional[str] = Form(None),
        file: Optional[UploadFile] = Form(None),
        session: Session = Depends(get_db)
):
    file_path = None

    if file:
        if not file.filename.endswith((".txt", ".pdf")):
            raise HTTPException(status_code=400, detail="Invalid file type")

        file_path = f"uploads/{file.filename}"
        with open(file_path, "wb") as f:
            f.write(file.file.read())

    input_service = InputDataService(session)
    input_service.create(
        input_data=InputDataInput(
            type=type,
            text=text,
            article_url=article_url,
            youtube_url=youtube_url,
            file_path=file_path
        )
    )
    return RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)


@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    return settings.TEMPLATES.TemplateResponse(request=request, name="home.html")
