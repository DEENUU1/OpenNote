from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from config.settings import settings
from views.router import router
from utils.init_app import init_app
import langchain


langchain.debug = False#settings.LANGCHAIN_DEBUG
init_app()

app = FastAPI(
    debug=settings.DEBUG,
    title=settings.TITLE,
)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app)

