"""Instant replies without OpenAI for greetings and simple FAQs."""

from __future__ import annotations

import re

from app.models import Tenant
from app.services.intent import ChatIntent, IntentResult

_GREETING_RE = re.compile(
    r"^(\s*)(hi|hello|hey|hiya|howdy|good\s+(morning|afternoon|evening)|"
    r"what'?s\s+up|yo|greetings)(\s*[!?.…]*)$",
    re.IGNORECASE,
)

_THANKS_RE = re.compile(
    r"^(\s*)(thanks|thank\s+you|thx|cheers|much\s+appreciated)(\s*[!?.…]*)$",
    re.IGNORECASE,
)

_BYE_RE = re.compile(
    r"^(\s*)(bye|goodbye|see\s+you|talk\s+later)(\s*[!?.…]*)$",
    re.IGNORECASE,
)

# Hours/contact fast path only for short, focused questions
_MAX_FAST_FAQ_LEN = 140


def _is_short(text: str) -> bool:
    return len(text) <= _MAX_FAST_FAQ_LEN


def _winner_clear(result: IntentResult, intent: ChatIntent) -> bool:
    if result.intent != intent:
        return False
    if result.confidence < 2:
        return False
    # Another intent nearly tied → use LLM
    others = [s for i, s in result.scores.items() if i != intent]
    if others and max(others) >= result.confidence - 1:
        return False
    return True


def try_fast_reply(tenant: Tenant, user_text: str, result: IntentResult) -> str | None:
    """
    Return an immediate reply string, or None to continue with LLM + enrichment.
    """
    text = (user_text or "").strip()
    if not text:
        return None

    name = tenant.display_name

    if _GREETING_RE.match(text):
        welcome = (tenant.welcome_message or "").strip()
        if welcome:
            return welcome
        return (
            f"Hello! Welcome to {name}. "
            "How can we help you today? Share your name and contact details if you'd like us to follow up."
        )

    if _THANKS_RE.match(text):
        return f"You're welcome! If you need anything else from {name}, just ask."

    if _BYE_RE.match(text):
        return f"Thanks for chatting with {name}. Use **End chat** when you're finished so we can save your conversation."

    if not _is_short(text):
        return None

    if _winner_clear(result, ChatIntent.HOURS_LOCATION):
        hours = (tenant.business_hours_text or "").strip()
        if hours:
            return f"Our opening hours: {hours}\n\nFor the full address and more details, check our website or ask another question."
        return f"Please contact {name} for our current opening hours and location."

    if _winner_clear(result, ChatIntent.CONTACT):
        parts: list[str] = [f"You can reach {name}:"]
        if tenant.contact_phone:
            parts.append(f"Phone: {tenant.contact_phone}")
        if tenant.contact_email_public:
            parts.append(f"Email: {tenant.contact_email_public}")
        if len(parts) == 1:
            return "Please use the contact details on our website — we don't have phone/email listed in chat yet."
        return "\n".join(parts)

    return None
