from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import get_settings
from app.database_info import database_backend, database_target_for_logs, normalize_database_url
from app.db import get_session
from app.schemas import HealthOut

router = APIRouter()


@router.get("/health", response_model=HealthOut)
async def health(session: AsyncSession = Depends(get_session)) -> HealthOut:
    url = normalize_database_url(get_settings().database_url)
    backend = database_backend(url)
    target = database_target_for_logs(url)
    try:
        await session.execute(text("SELECT 1"))
        return HealthOut(
            status="ok",
            database="connected",
            database_backend=backend,
            database_target=target,
        )
    except SQLAlchemyError:
        return HealthOut(
            status="degraded",
            database="disconnected",
            database_backend=backend,
            database_target=target,
        )
