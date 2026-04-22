import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base


def _uuid():
    return uuid.uuid4()


class Tenant(Base):
    __tablename__ = "tenants"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=_uuid)
    slug: Mapped[str] = mapped_column(String(80), unique=True, index=True)
    display_name: Mapped[str] = mapped_column(String(200))
    timezone: Mapped[str] = mapped_column(String(64), default="UTC")

    primary_color: Mapped[str] = mapped_column(String(32), default="#2563eb")
    background_color: Mapped[str] = mapped_column(String(32), default="#f8fafc")
    text_color: Mapped[str] = mapped_column(String(32), default="#0f172a")
    logo_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    welcome_message: Mapped[str] = mapped_column(String(500), default="How can we help you today?")

    faq_text: Mapped[str] = mapped_column(Text, default="")
    business_hours_text: Mapped[str] = mapped_column(String(2000), default="")
    contact_phone: Mapped[str | None] = mapped_column(String(64), nullable=True)
    contact_email_public: Mapped[str | None] = mapped_column(String(200), nullable=True)

    transcript_email: Mapped[str] = mapped_column(String(200), default="owner@example.com")

    sessions: Mapped[list["ChatSession"]] = relationship(back_populates="tenant")


class ChatSession(Base):
    __tablename__ = "chat_sessions"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=_uuid)
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("tenants.id"), index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    ended_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    end_reason: Mapped[str | None] = mapped_column(String(32), nullable=True)

    tenant: Mapped["Tenant"] = relationship(back_populates="sessions")
    messages: Mapped[list["ChatMessage"]] = relationship(
        back_populates="session", order_by="ChatMessage.created_at"
    )


class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=_uuid)
    session_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("chat_sessions.id"), index=True)
    role: Mapped[str] = mapped_column(String(16))
    content: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    session: Mapped["ChatSession"] = relationship(back_populates="messages")
