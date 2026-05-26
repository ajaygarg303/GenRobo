"""Close a chat session: persist summary and notify the business."""

from __future__ import annotations

import json
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import ChatMessage, ChatSession, Tenant
from app.services.session_summary import generate_session_summary
from app.services.transcript import send_transcript_if_configured


async def close_chat_session(
    session: AsyncSession,
    chat: ChatSession,
    tenant: Tenant,
    reason: str,
) -> None:
    if chat.ended_at is not None:
        return

    chat.ended_at = datetime.now(timezone.utc)
    chat.end_reason = reason
    await session.flush()

    result = await session.execute(
        select(ChatMessage).where(ChatMessage.session_id == chat.id).order_by(ChatMessage.created_at)
    )
    messages = list(result.scalars().all())

    summary, lead = await generate_session_summary(tenant, messages)
    chat.summary_text = summary
    chat.lead_json = json.dumps(lead, ensure_ascii=False)
    await session.commit()
    await session.refresh(chat)

    await send_transcript_if_configured(session, chat, tenant, summary=summary, lead=lead)
