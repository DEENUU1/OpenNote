from fastapi import Request, APIRouter, Depends, Form, UploadFile
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
from utils.upload_file import upload_file


router = APIRouter(
    prefix="",
    tags=["Input"],
)


@router.post("/input/{input_id}", status_code=303)
def delete_input_data(input_id: int, session: Session = Depends(get_db)):
    InputDataService(session).delete(input_id)
    return RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)


@router.post("/input", status_code=303)
def create_input_data(
        type: TypeEnum = Form(...),
        text: Optional[str] = Form(None),
        article_url: Optional[str] = Form(None),
        youtube_url: Optional[str] = Form(None),
        file: Optional[UploadFile] = Form(None),
        session: Session = Depends(get_db)
):
    uploaded_file = upload_file(file)

    InputDataService(session).create(
        input_data=InputDataInput(
            type=type,
            text=text,
            article_url=article_url,
            youtube_url=youtube_url,
            file_path=uploaded_file
        )
    )
    return RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)


@router.get("/", response_class=HTMLResponse)
def home(request: Request, session: Session = Depends(get_db)):
    input_list = InputDataService(session).get_all()

    return settings.TEMPLATES.TemplateResponse(
        request=request,
        name="home.html",
        context={
            "input_list": input_list,
        }
    )
