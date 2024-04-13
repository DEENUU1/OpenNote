from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from config.settings import settings
from views.router import router
from utils.init_app import init_app

init_app()

app = FastAPI(
    debug=settings.DEBUG,
    title=settings.TITLE,
)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(router)
