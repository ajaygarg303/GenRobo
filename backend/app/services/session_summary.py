"""Generate lead summary for closed chat sessions."""

from __future__ import annotations

import json
import logging

from openai import AsyncOpenAI

from app.config import get_settings
from app.models import ChatMessage, Tenant

logger = logging.getLogger(__name__)

_DEFAULT_LEAD = {
    "contact_name": None,
    "contact_phone": None,
    "contact_email": None,
    "intent": None,
    "notes": None,
}


def _openai_client() -> AsyncOpenAI | None:
    s = get_settings()
    if not s.openai_api_key:
        return None
    kwargs: dict[str, str] = {"api_key": s.openai_api_key}
    if s.openai_base_url.strip():
        kwargs["base_url"] = s.openai_base_url.rstrip("/")
    return AsyncOpenAI(**kwargs)


async def generate_session_summary(
    tenant: Tenant,
    messages: list[ChatMessage],
) -> tuple[str, dict]:
    """
    Return (summary_paragraph, lead_dict).
    Falls back to a simple transcript digest when OpenAI is not configured.
    """
    lines = [f"{m.role.upper()}: {m.content}" for m in messages if m.role in ("user", "assistant")]
    transcript = "\n".join(lines) or "(empty chat)"

    client = _openai_client()
    if client is None:
        summary = (
            f"Chat with {tenant.display_name} ended. "
            f"{len([m for m in messages if m.role == 'user'])} customer message(s). "
            "Configure OPENAI_API_KEY for AI-generated lead summaries."
        )
        return summary, dict(_DEFAULT_LEAD)

    system = (
        "You summarize business website chats for the owner. "
        "Respond with valid JSON only, no markdown fences. "
        'Schema: {"summary":"4-5 sentences for the business owner",'
        '"contact_name":string|null,"contact_phone":string|null,'
        '"contact_email":string|null,"intent":string|null,"notes":string|null}. '
        "Extract contact details only if the customer mentioned them. "
        "intent = what they wanted; notes = urgency or follow-up actions."
    )
    user = f"Business: {tenant.display_name}\n\nTranscript:\n{transcript[:12000]}"

    try:
        s = get_settings()
        resp = await client.chat.completions.create(
            model=s.openai_model,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            temperature=0.2,
            max_tokens=500,
            response_format={"type": "json_object"},
        )
        raw = (resp.choices[0].message.content or "").strip()
        data = json.loads(raw)
        summary = str(data.get("summary") or "").strip() or "Chat completed."
        lead = {
            "contact_name": data.get("contact_name"),
            "contact_phone": data.get("contact_phone"),
            "contact_email": data.get("contact_email"),
            "intent": data.get("intent"),
            "notes": data.get("notes"),
        }
        return summary, lead
    except Exception as e:
        logger.warning("Session summary generation failed: %s", e)
        return (
            f"Chat with {tenant.display_name} ended. See full transcript below.",
            dict(_DEFAULT_LEAD),
        )
