from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from starlette import status

from config.database import get_db
from services.input_service import InputDataService
from fastapi.responses import RedirectResponse
from tasks.preprocess import run_preprocess


router = APIRouter(
    prefix="/preprocess",
    tags=["Preprocess"],
)


@router.post("/{input_id}", status_code=303)
def run_preprocess_tasks(input_id: int, background_tasks: BackgroundTasks, session: Session = Depends(get_db)):
    input_details = InputDataService(session).get_details(input_id)
    background_tasks.add_task(run_preprocess, input_details, session)

    return RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)
