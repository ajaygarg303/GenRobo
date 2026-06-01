"""Intent classification with industry templates and per-tenant overrides."""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass
from enum import Enum

from app.models import Tenant
from app.services.intent_profiles import get_profile, resolve_business_type

logger = logging.getLogger(__name__)

# Re-export for other modules
__all__ = ["ChatIntent", "IntentResult", "classify_intent"]


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


def classify_intent(user_text: str, tenant: Tenant) -> IntentResult:
    """
    Score message against template keywords + tenant overrides.
    Highest score wins; ties lean to GENERAL.
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
