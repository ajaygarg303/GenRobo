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

# Hours fast path only for short, focused questions
_MAX_FAST_FAQ_LEN = 140


def _is_short(text: str) -> bool:
    return len(text) <= _MAX_FAST_FAQ_LEN


def _winner_clear(result: IntentResult, intent: ChatIntent) -> bool:
    if result.intent != intent:
        return False
    if result.confidence < 2:
        return False
    others = [s for i, s in result.scores.items() if i != intent]
    if others and max(others) >= result.confidence - 1:
        return False
    return True


def try_fast_reply(
    tenant: Tenant,
    user_text: str,
    result: IntentResult,
    *,
    conversation_started: bool = False,
) -> str | None:
    """
    Return an immediate reply string, or None to continue with LLM + enrichment.
    Contact and lead replies are left to the LLM so opening-message context is used.
    """
    text = (user_text or "").strip()
    if not text:
        return None

    name = tenant.display_name

    if _GREETING_RE.match(text):
        if conversation_started:
            return f"Hello! How can we help you at {name} today?"
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

    return None
