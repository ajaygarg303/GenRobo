from collections.abc import AsyncGenerator
from pathlib import Path

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.config import get_settings
from app.database_info import normalize_database_url


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
_database_url = normalize_database_url(_settings.database_url)
_ensure_sqlite_dir(_database_url)

engine = create_async_engine(
    _database_url,
    echo=False,
    future=True,
)

SessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session


