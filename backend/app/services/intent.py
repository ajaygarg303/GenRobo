"""Intent classification with industry templates and per-tenant overrides."""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass
from enum import Enum

from app.models import ChatMessage, Tenant
from app.services.intent_profiles import get_profile, resolve_business_type

logger = logging.getLogger(__name__)

# Re-export for other modules
__all__ = ["ChatIntent", "IntentResult", "classify_intent", "classify_intent_for_message"]


class ChatIntent(str, Enum):
    GENERAL = "general"
    STOCK_PRICE = "stock_price"
    MENU_ORDER = "menu_order"
    HOURS_LOCATION = "hours_location"
    CONTACT = "contact"


@dataclass(frozen=True)
class IntentResult:
    intent: ChatIntent
    confidence: int
    scores: dict[ChatIntent, int]
    business_type: str
    load_dynamic_data: bool = False


def _contains_any(text: str, keywords: frozenset[str]) -> bool:
    return any(k in text for k in keywords)


def _parse_tenant_keyword_overrides(tenant: Tenant) -> dict[ChatIntent, frozenset[str]]:
    raw = getattr(tenant, "intent_config_json", None) or "{}"
    try:
        data = json.loads(raw) if isinstance(raw, str) else {}
    except json.JSONDecodeError:
        logger.warning("Invalid intent_config_json for tenant %s", tenant.slug)
        return {}

    extra: dict[ChatIntent, set[str]] = {i: set() for i in ChatIntent}
    kw_block = data.get("keywords") if isinstance(data, dict) else None
    if not isinstance(kw_block, dict):
        return {}

    intent_map = {
        "stock_price": ChatIntent.STOCK_PRICE,
        "menu_order": ChatIntent.MENU_ORDER,
        "hours_location": ChatIntent.HOURS_LOCATION,
        "contact": ChatIntent.CONTACT,
        "general": ChatIntent.GENERAL,
    }
    for key, words in kw_block.items():
        intent = intent_map.get(str(key).lower())
        if intent is None or not isinstance(words, list):
            continue
        extra[intent].update(str(w).lower() for w in words if w)

    return {k: frozenset(v) for k, v in extra.items() if v}


async def classify_intent_for_message(
    tenant: Tenant,
    user_text: str,
    history: list[ChatMessage],
) -> IntentResult:
    """Prefer LLM classification with conversation context; fall back to keywords in mock/offline mode."""
    from app.services.intent_llm import classify_intent_llm

    llm_result = await classify_intent_llm(tenant, user_text, history)
    if llm_result is not None:
        return llm_result
    return classify_intent_keywords(user_text, tenant)


def classify_intent(user_text: str, tenant: Tenant) -> IntentResult:
    """Keyword fallback (sync). Used when LLM path is not available."""
    return classify_intent_keywords(user_text, tenant)


def classify_intent_keywords(user_text: str, tenant: Tenant) -> IntentResult:
    """
    Score message against template keywords + tenant overrides.
    Highest score wins; ties lean to GENERAL. Fallback only — prefer classify_intent_for_message.
    """
    text = (user_text or "").lower().strip()
    business_type = resolve_business_type(
        tenant.slug,
        getattr(tenant, "business_type", None),
    )
    profile = get_profile(business_type)
    overrides = _parse_tenant_keyword_overrides(tenant)

    scores: dict[ChatIntent, int] = {i: 0 for i in ChatIntent}

    for intent_key, keywords in profile.keywords.items():
        try:
            intent_enum = ChatIntent(intent_key)
        except ValueError:
            continue
        if _contains_any(text, keywords):
            scores[intent_enum] += 2
        extra = overrides.get(intent_enum)
        if extra and _contains_any(text, extra):
            scores[intent_enum] += 2

    # Slug-specific nudges (until all tenants use business_type + config)
    if tenant.slug == "siyu":
        if any(w in text for w in ("iphone", "samsung", "galaxy", "pixel", "watch", "charger", "case")):
            scores[ChatIntent.STOCK_PRICE] += 2
    if tenant.slug == "india-gate":
        if any(w in text for w in ("chicken", "lamb", "paneer", "prawn", "tikka", "korma")):
            scores[ChatIntent.MENU_ORDER] += 2

    # Service/repair questions are not "how do I contact you?"
    if any(w in text for w in ("repair", "repairs", "fix", "fixed", "broken", "cracked", "warranty")):
        scores[ChatIntent.GENERAL] += 2

    best = max(scores, key=lambda k: scores[k])
    confidence = scores[best]
    if confidence == 0:
        return IntentResult(
            intent=ChatIntent.GENERAL,
            confidence=0,
            scores=scores,
            business_type=business_type,
        )
    return IntentResult(
        intent=best,
        confidence=confidence,
        scores=scores,
        business_type=business_type,
    )
