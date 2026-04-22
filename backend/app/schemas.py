from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, Field


class TenantPublicConfig(BaseModel):
    slug: str
    display_name: str
    timezone: str
    primary_color: str
    background_color: str
    text_color: str
    logo_url: str | None
    welcome_message: str
    business_hours_text: str
    contact_phone: str | None
    contact_email_public: str | None


class SessionCreate(BaseModel):
    tenant_slug: str = Field(min_length=1, max_length=80)


class SessionOut(BaseModel):
    id: UUID
    tenant_slug: str


class MessageIn(BaseModel):
    content: str = Field(min_length=1, max_length=8000)


class MessageOut(BaseModel):
    role: str
    content: str


class ChatTurnResponse(BaseModel):
    assistant_message: MessageOut


class EndSessionBody(BaseModel):
    reason: Literal["user", "timeout"] = "user"


class HealthOut(BaseModel):
    status: str
    database: str


class TranscriptLine(BaseModel):
    role: str
    content: str
    created_at: datetime | None = None
