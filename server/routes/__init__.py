from fastapi import APIRouter
from .openrouter import router as openrouter_router

main_router = APIRouter()

main_router.include_router(openrouter_router, tags=['OpenRouter Endpoint'])
