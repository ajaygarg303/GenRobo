"""Instant replies without OpenAI for greetings and simple FAQs."""

from __future__ import annotations

import re

from app.models import Tenant

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

def try_fast_reply(
    tenant: Tenant,
    user_text: str,
    *,
    conversation_started: bool = False,
) -> str | None:
    """
    Instant replies for pure greetings/thanks/goodbye only — everything else uses the LLM.
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

    return None
