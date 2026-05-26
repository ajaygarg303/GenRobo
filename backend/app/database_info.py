"""Helpers to report which database backend is in use (no credentials in logs)."""


def normalize_database_url(url: str) -> str:
    """
    Make DATABASE_URL work with SQLAlchemy create_async_engine.

    - postgresql:// or postgres:// → postgresql+asyncpg:// (required for this app)
    - Adds ssl=require for RDS when no ssl/sslmode query param is present
    """
    u = url.strip()
    if not u:
        return u

    if u.startswith("postgresql://"):
        u = "postgresql+asyncpg://" + u[len("postgresql://") :]
    elif u.startswith("postgres://"):
        u = "postgresql+asyncpg://" + u[len("postgres://") :]

    low = u.lower()
    if low.startswith("postgresql+asyncpg://"):
        if "ssl=" not in low and "sslmode=" not in low:
            u = f"{u}{'&' if '?' in u else '?'}ssl=require"

    return u


def database_backend(url: str) -> str:
    low = url.lower()
    if "sqlite" in low:
        return "sqlite"
    if "postgresql" in low or "postgres" in low:
        return "postgresql"
    return "other"


def database_target_for_logs(url: str) -> str:
    """Host/database for Postgres, or file path for SQLite — safe to log."""
    if "sqlite" in url.lower():
        marker = "sqlite+aiosqlite:///"
        if marker in url:
            return f"sqlite:{url.split(marker, 1)[1].split('?')[0]}"
        return "sqlite:local"

    if "://" not in url:
        return "unknown"

    rest = url.split("://", 1)[1]
    if "@" in rest:
        rest = rest.split("@", 1)[1]
    host_part = rest.split("/", 1)[0].split("?")[0]
    if "/" in rest:
        db_name = rest.split("/", 1)[1].split("?")[0]
        return f"{host_part}/{db_name}"
    return host_part
