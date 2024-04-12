from fastapi import APIRouter
from . import input_view

router = APIRouter(
    prefix=""
)

router.include_router(input_view.router)
