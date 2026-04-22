import logging
import smtplib
from email.message import EmailMessage

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import get_settings
from app.models import ChatMessage, ChatSession, Tenant

logger = logging.getLogger(__name__)


async def send_transcript_if_configured(
    session: AsyncSession,
    chat: ChatSession,
    tenant: Tenant,
) -> None:
    result = await session.execute(
        select(ChatMessage).where(ChatMessage.session_id == chat.id).order_by(ChatMessage.created_at)
    )
    rows = result.scalars().all()
    lines = []
    for m in rows:
        if m.role in ("user", "assistant"):
            lines.append(f"{m.role.upper()}: {m.content}")

    body = (
        f"Chat transcript for {tenant.display_name}\n"
        f"Session ID: {chat.id}\n"
        f"Ended: {chat.end_reason}\n\n"
        + "\n\n".join(lines)
    )

    logger.info("Transcript (session %s):\n%s", chat.id, body)

    s = get_settings()
    if not s.smtp_host or not tenant.transcript_email:
        return

    msg = EmailMessage()
    msg["Subject"] = f"[{tenant.display_name}] New chat transcript"
    msg["From"] = s.smtp_from or s.smtp_user or "noreply@localhost"
    msg["To"] = tenant.transcript_email
    msg.set_content(body)

    try:
        with smtplib.SMTP(s.smtp_host, s.smtp_port) as smtp:
            smtp.starttls()
            if s.smtp_user and s.smtp_password:
                smtp.login(s.smtp_user, s.smtp_password)
            smtp.send_message(msg)
    except OSError as e:
        logger.warning("SMTP transcript send failed: %s", e)
