from fastapi import Request, APIRouter, Depends, Form, UploadFile, BackgroundTasks
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from starlette import status
from config.database import get_db
from config.settings import settings
from schemas.input_schema import InputDataInput
from services.input_service import InputDataService
from models.input import TypeEnum, TranscriptionType, Language
from typing import Optional
from fastapi.responses import RedirectResponse

from tasks.preprocess_youtube_channel import run_youtube_channel_preprocess
from tasks.preprocess_youtube_playlist import run_youtube_playlist_preprocess
from utils.upload_file import upload_file
from tasks.preprocess import run_preprocess


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
        background_tasks: BackgroundTasks,
        type_: TypeEnum = Form(...),
        text: Optional[str] = Form(None),
        article_url: Optional[str] = Form(None),
        youtube_url: Optional[str] = Form(None),
        youtube_channel: Optional[str] = Form(None),
        youtube_playlist: Optional[str] = Form(None),
        file: Optional[UploadFile] = Form(None),
        transcription_type: Optional[TranscriptionType] = Form(None),
        language: Optional[Language] = Form(None),
        session: Session = Depends(get_db)
):
    if youtube_channel:
        background_tasks.add_task(
            run_youtube_channel_preprocess,
            youtube_url,
            type_,
            language,
            transcription_type,
            session
        )
        return RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)

    if youtube_playlist:
        background_tasks.add_task(
            run_youtube_playlist_preprocess,
            youtube_url,
            type_,
            language,
            transcription_type,
            session
        )
        return RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)

    uploaded_file = upload_file(file)

    service = InputDataService(session)

    created_input = service.create(
        input_data=InputDataInput(
            type=type_,
            text=text,
            article_url=article_url,
            youtube_url=youtube_url,
            file_path=uploaded_file,
            language=language,
            transcription_type=transcription_type
        )
    )

    background_tasks.add_task(run_preprocess, created_input, session)
    return RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)


@router.get("/", response_class=HTMLResponse)
def input_list(request: Request, session: Session = Depends(get_db)):
    inputs = InputDataService(session).get_all()

    return settings.TEMPLATES.TemplateResponse(
        request=request,
        name="home.html",
        context={
            "input_list": inputs,
        }
    )


@router.get("/{input_id}", response_class=HTMLResponse)
def input_details(input_id: int, request: Request, session: Session = Depends(get_db)):
    details = InputDataService(session).get_details(input_id)

    return settings.TEMPLATES.TemplateResponse(
        request=request,
        name="details.html",
        context={
            "details": details,
        }
    )