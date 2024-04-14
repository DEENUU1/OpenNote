from fastapi import APIRouter, Depends, Form
from sqlalchemy.orm import Session
from starlette import status

from config.database import get_db
from fastapi.responses import RedirectResponse
from models.result import TypeEnum
from schemas.result_schema import ResultInput
from services.result_service import ResultService


router = APIRouter(
    prefix="/result",
    tags=["Result"],
)


@router.post("/{input_id}", status_code=303)
def generate_result(input_id: int, result_type: TypeEnum = Form(...), session: Session = Depends(get_db)):
    ResultService(session).create(
        ResultInput(
            input_id=input_id,
            type=result_type
        )
    )
    return RedirectResponse(f"/{input_id}", status_code=status.HTTP_303_SEE_OTHER)
