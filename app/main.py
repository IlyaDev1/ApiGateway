from fastapi import FastAPI
from uvicorn import run

from app.api.router import api_router
from app.core.config import settings_instance
from logger import logger

app = FastAPI()

app.include_router(api_router, prefix="/")


if __name__ == "__main__":
    run(
        "main:app",
        reload=False,
        host="0.0.0.0",
        port=settings_instance.APP_HOST_PORT,
    )
