from fastapi import Request, APIRouter
from fastapi.responses import HTMLResponse

from config.settings import settings

router = APIRouter(
    prefix="",
    tags=["Home"],
)


@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    return settings.TEMPLATES.TemplateResponse(request=request, name="home.html")
