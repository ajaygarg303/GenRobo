from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "Business Chatbot"
    database_url: str = "sqlite+aiosqlite:///./data/app.db"
    cors_origins: str = ""  # comma-separated; set CORS_ORIGINS when UI is on another origin

    openai_api_key: str = Field(default="", validation_alias="OPENAI_API_KEY")
    openai_model: str = Field(default="gpt-4o-mini", validation_alias="OPENAI_MODEL")
    # Optional: OpenAI-compatible API base (default is platform.openai.com)
    openai_base_url: str = Field(default="", validation_alias="OPENAI_BASE_URL")

    session_idle_timeout_minutes: int = 30
    smtp_host: str = ""
    smtp_port: int = 587
    smtp_user: str = ""
    smtp_password: str = ""
    smtp_from: str = ""

    # Shared S3 bucket for tenant knowledge-base objects; object key per tenant in DB.
    knowledge_s3_bucket: str = Field(default="", validation_alias="KNOWLEDGE_S3_BUCKET")
    # Optional: redis://host:6379/0 — when set, KB text is cached after successful S3 read.
    redis_url: str = Field(default="", validation_alias="REDIS_URL")
    kb_cache_ttl_seconds: int = Field(default=1800, validation_alias="KB_CACHE_TTL_SECONDS")


@lru_cache
def get_settings() -> Settings:
    return Settings()
