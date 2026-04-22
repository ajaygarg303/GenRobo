import logging
import os
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.config import get_settings
from app.db import Base, engine
from app.routers import chat, health, tenants
from app.seed import seed

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

STATIC_DIR = Path(__file__).resolve().parent / "static"


@asynccontextmanager
async def lifespan(_: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await seed()
    yield


def create_app() -> FastAPI:
    settings = get_settings()
    enable_docs = os.getenv("ENABLE_DOCS", "true").lower() in ("1", "true", "yes")
    app = FastAPI(
        title=settings.app_name,
        lifespan=lifespan,
        docs_url="/docs" if enable_docs else None,
        redoc_url="/redoc" if enable_docs else None,
        openapi_url="/openapi.json" if enable_docs else None,
    )

    origins = [o.strip() for o in settings.cors_origins.split(",") if o.strip()]
    if origins:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    app.include_router(health.router, prefix="/api")
    app.include_router(tenants.router, prefix="/api")
    app.include_router(chat.router, prefix="/api")

    if STATIC_DIR.is_dir() and (STATIC_DIR / "index.html").is_file():
        assets = STATIC_DIR / "assets"
        if assets.is_dir():
            app.mount("/assets", StaticFiles(directory=assets), name="assets")

        @app.get("/{full_path:path}")
        async def spa(full_path: str):
            if full_path.startswith("api"):
                from fastapi import HTTPException

                raise HTTPException(status_code=404, detail="Not found")
            index = STATIC_DIR / "index.html"
            if not index.is_file():
                from fastapi import HTTPException

                raise HTTPException(status_code=404, detail="Not found")
            return FileResponse(index)

    return app


app = create_app()
