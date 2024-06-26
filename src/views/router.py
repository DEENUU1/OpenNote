from fastapi import APIRouter
from . import input_view, preprocess_view, process_view

router = APIRouter(
    prefix=""
)

router.include_router(input_view.router)
router.include_router(preprocess_view.router)
router.include_router(process_view.router)

