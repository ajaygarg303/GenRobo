from collections.abc import AsyncGenerator
from pathlib import Path

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.config import get_settings


class Base(DeclarativeBase):
    pass


def _ensure_sqlite_dir(url: str) -> None:
    if "sqlite" not in url:
        return
    marker = "sqlite+aiosqlite:///"
    if marker not in url:
        return
    path_part = url.split(marker, 1)[1]
    parent = Path(path_part).resolve().parent
    parent.mkdir(parents=True, exist_ok=True)


_settings = get_settings()
_ensure_sqlite_dir(_settings.database_url)

engine = create_async_engine(
    _settings.database_url,
    echo=False,
    future=True,
)

SessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session


async def ensure_tenant_knowledge_s3_key_column() -> None:
    """Add knowledge_s3_key to tenants on existing DBs (create_all does not alter columns)."""
    url = _settings.database_url.lower()
    async with engine.begin() as conn:
        if "postgresql" in url or "postgres" in url:
            await conn.execute(
                text(
                    "ALTER TABLE tenants ADD COLUMN IF NOT EXISTS "
                    "knowledge_s3_key VARCHAR(1024)"
                )
            )
        elif "sqlite" in url:
            r = await conn.execute(text("PRAGMA table_info(tenants)"))
            cols = [row[1] for row in r.fetchall()]
            if cols and "knowledge_s3_key" not in cols:
                await conn.execute(
                    text("ALTER TABLE tenants ADD COLUMN knowledge_s3_key VARCHAR(1024)")
                )
