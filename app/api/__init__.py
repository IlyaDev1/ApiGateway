"""
В __init__ предлагается объединять все роутеры, чтобы получить итоговый роутер api_router
"""

from fastapi import APIRouter

from .router import api_router

main_api_router = APIRouter()
main_api_router.include_router(api_router, prefix="/v1")
