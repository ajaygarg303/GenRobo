from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_session
from app.schemas import HealthOut

router = APIRouter()


@router.get("/health", response_model=HealthOut)
async def health(session: AsyncSession = Depends(get_session)) -> HealthOut:
    try:
        await session.execute(text("SELECT 1"))
        return HealthOut(status="ok", database="connected")
    except SQLAlchemyError:
        return HealthOut(status="degraded", database="disconnected")
