"""Close a chat session: persist summary and notify the business."""

from __future__ import annotations

import json
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import ChatMessage, ChatSession, Tenant
from app.services.session_summary import generate_session_summary
from app.services.transcript import schedule_transcript_email


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
    if getattr(chat, "visitor_email", None) and not lead.get("contact_email"):
        lead["contact_email"] = chat.visitor_email
    if getattr(chat, "visitor_phone", None) and not lead.get("contact_phone"):
        lead["contact_phone"] = chat.visitor_phone
    if getattr(chat, "visitor_name", None) and not lead.get("contact_name"):
        lead["contact_name"] = chat.visitor_name
    chat.summary_text = summary
    chat.lead_json = json.dumps(lead, ensure_ascii=False)
    await session.commit()
    await session.refresh(chat)

    schedule_transcript_email(tenant, chat, messages, summary=summary, lead=lead)
