"""Chat transcript logging and optional SMTP delivery."""

from __future__ import annotations

import asyncio
import logging
import smtplib
from email.message import EmailMessage
from typing import Any
from uuid import UUID

from app.config import Settings, get_settings
from app.models import ChatMessage, ChatSession, Tenant

logger = logging.getLogger(__name__)


def _format_lead_block(lead: dict[str, Any]) -> str:
    lines = ["--- Lead summary ---"]
    for key, label in (
        ("contact_name", "Name"),
        ("contact_phone", "Phone"),
        ("contact_email", "Email"),
        ("intent", "Looking for"),
        ("notes", "Notes"),
    ):
        val = lead.get(key)
        if val:
            lines.append(f"{label}: {val}")
    if len(lines) == 1:
        lines.append("(No contact details captured in chat.)")
    return "\n".join(lines)


def build_visitor_transcript_body(
    *,
    messages: list[ChatMessage],
    summary: str,
) -> str:
    lines = [
        f"{m.role.upper()}: {m.content}"
        for m in messages
        if m.role in ("user", "assistant")
    ]
    return (
        "Thanks for trying MyRoboChat!\n\n"
        "Below is a copy of your demo chat. Answers were generated from our sample "
        "business knowledge base only.\n\n"
        f"--- Summary ---\n{summary}\n\n"
        f"--- Full transcript ---\n"
        + "\n\n".join(lines)
        + "\n\n---\n"
        "Interested in a branded assistant for your business? Reply to this email or visit myrobochat.com.\n"
    )


def build_transcript_body(
    *,
    tenant_display_name: str,
    session_id: UUID,
    end_reason: str | None,
    messages: list[ChatMessage],
    summary: str,
    lead: dict[str, Any],
) -> str:
    lines = [
        f"{m.role.upper()}: {m.content}"
        for m in messages
        if m.role in ("user", "assistant")
    ]
    lead_block = _format_lead_block(lead)
    return (
        f"Chat transcript for {tenant_display_name}\n"
        f"Session ID: {session_id}\n"
        f"Ended: {end_reason}\n\n"
        f"{lead_block}\n\n"
        f"--- Summary ---\n{summary}\n\n"
        f"--- Full transcript ---\n"
        + "\n\n".join(lines)
    )


def _smtp_send_sync(
    settings: Settings,
    *,
    to_email: str,
    display_name: str,
    body: str,
    subject: str | None = None,
) -> None:
    """Blocking SMTP send — always run via asyncio.to_thread from async code."""
    timeout = settings.smtp_timeout_seconds
    msg = EmailMessage()
    msg["Subject"] = subject or f"[{display_name}] Chat lead & transcript"
    msg["From"] = settings.smtp_from or settings.smtp_user or "noreply@localhost"
    msg["To"] = to_email
    msg.set_content(body)

    with smtplib.SMTP(settings.smtp_host, settings.smtp_port, timeout=timeout) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        if settings.smtp_user and settings.smtp_password:
            smtp.login(settings.smtp_user, settings.smtp_password)
        smtp.send_message(msg)


async def _background_smtp_send(
    settings: Settings,
    *,
    to_email: str,
    display_name: str,
    body: str,
    session_id: UUID,
    subject: str | None = None,
) -> None:
    try:
        await asyncio.to_thread(
            _smtp_send_sync,
            settings,
            to_email=to_email,
            display_name=display_name,
            body=body,
            subject=subject,
        )
        logger.info("Transcript email sent for session %s to %s", session_id, to_email)
    except Exception as e:
        logger.warning(
            "SMTP transcript send failed for session %s (host=%s port=%s): %s",
            session_id,
            settings.smtp_host,
            settings.smtp_port,
            e,
        )


def schedule_transcript_email(
    tenant: Tenant,
    chat: ChatSession,
    messages: list[ChatMessage],
    *,
    summary: str,
    lead: dict[str, Any],
) -> None:
    """
    Log transcript and queue SMTP in the background so /end returns immediately.
    Avoids blocking the event loop (ECS health checks) on slow or unreachable SMTP.
    """
    summary_text = summary or chat.summary_text or "(No summary generated.)"
    body = build_transcript_body(
        tenant_display_name=tenant.display_name,
        session_id=chat.id,
        end_reason=chat.end_reason,
        messages=messages,
        summary=summary_text,
        lead=lead or {},
    )
    logger.info("Transcript ready for session %s (%d messages)", chat.id, len(messages))

    settings = get_settings()
    to_email = (tenant.transcript_email or "").strip()
    if not settings.smtp_host.strip():
        logger.info(
            "Transcript email skipped for session %s (SMTP_HOST not set; see CloudWatch for transcript)",
            chat.id,
        )
        return
    if not to_email:
        logger.info("Transcript email skipped for session %s (tenant transcript_email empty)", chat.id)
        return

    asyncio.create_task(
        _background_smtp_send(
            settings,
            to_email=to_email,
            display_name=tenant.display_name,
            body=body,
            session_id=chat.id,
        )
    )

    visitor_email = (getattr(chat, "visitor_email", None) or "").strip()
    if visitor_email and visitor_email.lower() != to_email.lower():
        visitor_body = build_visitor_transcript_body(messages=messages, summary=summary_text)
        asyncio.create_task(
            _background_smtp_send(
                settings,
                to_email=visitor_email,
                display_name="MyRoboChat Demo",
                body=visitor_body,
                session_id=chat.id,
                subject="Your MyRoboChat demo transcript",
            )
        )
