from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "Business Chatbot"
    database_url: str = "sqlite+aiosqlite:///./data/app.db"
    cors_origins: str = ""  # comma-separated; set CORS_ORIGINS when UI is on another origin

    openai_api_key: str = ""
    openai_model: str = "gpt-4o-mini"
    # Optional: OpenAI-compatible API base (default is platform.openai.com)
    openai_base_url: str = ""

    session_idle_timeout_minutes: int = 30
    smtp_host: str = ""
    smtp_port: int = 587
    smtp_user: str = ""
    smtp_password: str = ""
    smtp_from: str = ""


@lru_cache
def get_settings() -> Settings:
    return Settings()
