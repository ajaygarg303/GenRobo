from datetime import datetime, timedelta, timezone
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.config import get_settings
from app.db import get_session
from app.models import ChatMessage, ChatSession, Tenant
from app.schemas import ChatTurnResponse, EndSessionBody, MessageIn, MessageOut, SessionCreate, SessionOut
from app.services.llm import generate_reply
from app.services.transcript import send_transcript_if_configured

router = APIRouter(prefix="/sessions", tags=["chat"])


async def _get_active_session(
    session: AsyncSession, session_id: UUID
) -> tuple[ChatSession, Tenant]:
    r = await session.execute(
        select(ChatSession)
        .options(selectinload(ChatSession.tenant))
        .where(ChatSession.id == session_id)
    )
    chat = r.scalar_one_or_none()
    if not chat:
        raise HTTPException(status_code=404, detail="Session not found")
    if chat.ended_at is not None:
        raise HTTPException(status_code=410, detail="Session has ended")
    return chat, chat.tenant


def _check_idle(last_message_at: datetime | None, idle_minutes: int) -> bool:
    if last_message_at is None:
        return False
    now = datetime.now(timezone.utc)
    if last_message_at.tzinfo is None:
        last_message_at = last_message_at.replace(tzinfo=timezone.utc)
    return now - last_message_at > timedelta(minutes=idle_minutes)


@router.post("", response_model=SessionOut)
async def create_session(
    body: SessionCreate,
    session: AsyncSession = Depends(get_session),
) -> SessionOut:
    r = await session.execute(select(Tenant).where(Tenant.slug == body.tenant_slug))
    tenant = r.scalar_one_or_none()
    if not tenant:
        raise HTTPException(status_code=404, detail="Business not found")

    chat = ChatSession(tenant_id=tenant.id)
    session.add(chat)
    await session.commit()
    await session.refresh(chat)
    return SessionOut(id=chat.id, tenant_slug=tenant.slug)


@router.post("/{session_id}/message", response_model=ChatTurnResponse)
async def post_message(
    session_id: UUID,
    body: MessageIn,
    session: AsyncSession = Depends(get_session),
) -> ChatTurnResponse:
    settings = get_settings()
    chat, tenant = await _get_active_session(session, session_id)

    r = await session.execute(
        select(ChatMessage)
        .where(ChatMessage.session_id == chat.id)
        .order_by(ChatMessage.created_at.desc())
        .limit(1)
    )
    last = r.scalar_one_or_none()
    last_at = last.created_at if last else None
    if _check_idle(last_at, settings.session_idle_timeout_minutes):
        chat.ended_at = datetime.now(timezone.utc)
        chat.end_reason = "timeout"
        await session.commit()
        await send_transcript_if_configured(session, chat, tenant)
        raise HTTPException(status_code=410, detail="Session timed out — start a new chat")

    user_msg = ChatMessage(session_id=chat.id, role="user", content=body.content)
    session.add(user_msg)
    await session.flush()

    hist = await session.execute(
        select(ChatMessage)
        .where(ChatMessage.session_id == chat.id)
        .where(ChatMessage.created_at <= user_msg.created_at)
        .order_by(ChatMessage.created_at)
    )
    history = list(hist.scalars().all())

    text = await generate_reply(tenant, history[:-1], body.content)
    asst = ChatMessage(session_id=chat.id, role="assistant", content=text)
    session.add(asst)
    await session.commit()

    return ChatTurnResponse(assistant_message=MessageOut(role="assistant", content=text))


@router.post("/{session_id}/end", status_code=204)
async def end_session(
    session_id: UUID,
    body: EndSessionBody,
    session: AsyncSession = Depends(get_session),
) -> None:
    chat, tenant = await _get_active_session(session, session_id)
    chat.ended_at = datetime.now(timezone.utc)
    chat.end_reason = body.reason
    await session.commit()
    await send_transcript_if_configured(session, chat, tenant)
