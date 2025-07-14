from fastapi import APIRouter
from .openrouter import router as openrouter_router
from .financial_calculations import router as financial_router

main_router = APIRouter()

main_router.include_router(openrouter_router, tags=['OpenRouter Endpoint'])
main_router.include_router(financial_router, tags=['Financial Calculations Endpoint'])
