from fastapi import APIRouter
from . import input_view, preprocess_view

router = APIRouter(
    prefix=""
)

router.include_router(input_view.router)
router.include_router(preprocess_view.router)
