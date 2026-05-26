"""Incremental schema updates for existing databases (create_all does not alter tables)."""

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncConnection

from app.database_info import database_backend
from app.db import _database_url, engine


async def _pg_add_column(conn: AsyncConnection, table: str, column: str, col_type: str) -> None:
    await conn.execute(text(f"ALTER TABLE {table} ADD COLUMN IF NOT EXISTS {column} {col_type}"))


async def _sqlite_has_column(conn: AsyncConnection, table: str, column: str) -> bool:
    r = await conn.execute(text(f"PRAGMA table_info({table})"))
    return column in [row[1] for row in r.fetchall()]


async def _sqlite_add_column(conn: AsyncConnection, table: str, column: str, col_type: str) -> None:
    if not await _sqlite_has_column(conn, table, column):
        await conn.execute(text(f"ALTER TABLE {table} ADD COLUMN {column} {col_type}"))


async def ensure_phase1_schema() -> None:
    backend = database_backend(_database_url)
    async with engine.begin() as conn:
        if backend == "postgresql":
            await _pg_add_column(conn, "tenants", "knowledge_s3_key", "VARCHAR(1024)")
            await _pg_add_column(conn, "tenants", "status", "VARCHAR(32) DEFAULT 'active'")
            await _pg_add_column(conn, "tenants", "plan_id", "UUID")
            await _pg_add_column(conn, "tenants", "subscription_ends_at", "TIMESTAMPTZ")
            await _pg_add_column(conn, "chat_sessions", "summary_text", "TEXT")
            await _pg_add_column(conn, "chat_sessions", "lead_json", "TEXT")
        elif backend == "sqlite":
            await _sqlite_add_column(conn, "tenants", "knowledge_s3_key", "VARCHAR(1024)")
            await _sqlite_add_column(conn, "tenants", "status", "VARCHAR(32) DEFAULT 'active'")
            await _sqlite_add_column(conn, "tenants", "plan_id", "VARCHAR(36)")
            await _sqlite_add_column(conn, "tenants", "subscription_ends_at", "DATETIME")
            await _sqlite_add_column(conn, "chat_sessions", "summary_text", "TEXT")
            await _sqlite_add_column(conn, "chat_sessions", "lead_json", "TEXT")
