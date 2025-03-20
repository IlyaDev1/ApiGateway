from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncSession

from .database import SessionLocal


@asynccontextmanager
async def get_db() -> AsyncSession:
    async with SessionLocal() as db:
        yield db
