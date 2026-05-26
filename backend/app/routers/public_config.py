from fastapi import APIRouter

from app.config import get_settings
from app.schemas import ChatSettingsOut

router = APIRouter(prefix="/public", tags=["public"])


@router.get("/chat-settings", response_model=ChatSettingsOut)
async def chat_settings() -> ChatSettingsOut:
    s = get_settings()
    return ChatSettingsOut(
        idle_reminder_seconds=s.chat_idle_reminder_seconds,
        idle_end_after_reminder_seconds=s.chat_idle_end_after_reminder_seconds,
        idle_reminder_message=s.chat_idle_reminder_message,
    )
