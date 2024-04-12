from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from config.settings import settings
from views.router import router
from models.input import InputData
from models.processed import ProcessedData
from models.preprocess import PreprocessData
from config.database import engine


InputData.metadata.create_all(bind=engine)
ProcessedData.metadata.create_all(bind=engine)
PreprocessData.metadata.create_all(bind=engine)

app = FastAPI(
    debug=settings.DEBUG,
    title=settings.TITLE,
)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(router)