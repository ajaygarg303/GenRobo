"""Load static FAQ vs dynamic operational data based on chat intent."""

from __future__ import annotations

import json
import logging

from app.models import Tenant
from app.services.intent import ChatIntent, IntentResult
from app.services.intent_profiles import get_profile
from app.services.knowledge import load_static_knowledge, strip_embedded_data_blocks

logger = logging.getLogger(__name__)

# Intents that may load dynamic_data_s3_key when configured
DYNAMIC_INTENTS_BY_BUSINESS: dict[str, frozenset[ChatIntent]] = {
    "retail_electronics": frozenset({ChatIntent.STOCK_PRICE}),
    "retail": frozenset({ChatIntent.STOCK_PRICE}),
    "restaurant": frozenset(),  # menu stays in static KB; add slots later
    "food": frozenset(),
    "general": frozenset(),
    "services": frozenset(),  # future: appointment intent
}


def resolve_dynamic_data_kind(tenant: Tenant) -> str:
    explicit = (getattr(tenant, "dynamic_data_kind", None) or "").strip().lower()
    if explicit and explicit != "none":
        return explicit
    raw = getattr(tenant, "intent_config_json", None) or "{}"
    try:
        data = json.loads(raw) if isinstance(raw, str) else {}
        dyn = data.get("dynamic") if isinstance(data, dict) else None
        if isinstance(dyn, dict) and dyn.get("kind"):
            return str(dyn["kind"]).lower()
    except json.JSONDecodeError:
        pass
    if (getattr(tenant, "dynamic_data_s3_key", None) or "").strip():
        return "inventory_csv"
    return "none"


def resolve_dynamic_data_s3_key(tenant: Tenant) -> str | None:
    key = (getattr(tenant, "dynamic_data_s3_key", None) or "").strip()
    if key:
        return key
    raw = getattr(tenant, "intent_config_json", None) or "{}"
    try:
        data = json.loads(raw) if isinstance(raw, str) else {}
        dyn = data.get("dynamic") if isinstance(data, dict) else None
        if isinstance(dyn, dict) and dyn.get("s3_key"):
            return str(dyn["s3_key"]).strip()
    except json.JSONDecodeError:
        pass
    # Legacy: sibling of knowledge.md
    kb = (tenant.knowledge_s3_key or "").strip()
    if kb.endswith("knowledge.md"):
        return kb[: -len("knowledge.md")] + "inventory.csv"
    if kb and "/" in kb:
        return kb.rsplit("/", 1)[0] + "/inventory.csv"
    slug = (tenant.slug or "").strip()
    return f"tenants/{slug}/inventory.csv" if slug else None


_PRODUCT_HINTS = (
    "iphone",
    "samsung",
    "galaxy",
    "pixel",
    "xiaomi",
    "poco",
    "garett",
    "charger",
    "case",
    "watch",
    "earbuds",
    "vacuum",
)


def _looks_like_product_query(text: str) -> bool:
    t = (text or "").lower()
    return any(h in t for h in _PRODUCT_HINTS)


def should_load_dynamic_data(
    tenant: Tenant,
    intent_result: IntentResult,
    user_text: str = "",
) -> bool:
    """
    Dynamic file is loaded when the classifier says so (LLM) or keyword fallback matches.
    """
    kind = resolve_dynamic_data_kind(tenant)
    if kind == "none":
        return False
    key = resolve_dynamic_data_s3_key(tenant)
    if not key:
        return False

    from app.services.intent_llm import LLM_CONFIDENCE

    if intent_result.confidence >= LLM_CONFIDENCE:
        return intent_result.load_dynamic_data

    profile = get_profile(intent_result.business_type)
    allowed = DYNAMIC_INTENTS_BY_BUSINESS.get(
        profile.business_type,
        frozenset(),
    )
    if intent_result.intent in allowed and intent_result.confidence >= 2:
        return True
    # Retail: still load stock file when message clearly mentions products
    if profile.business_type in ("retail_electronics", "retail") and _looks_like_product_query(user_text):
        return True
    return False


async def load_static_for_intent(tenant: Tenant, intent: ChatIntent) -> str:
    """
    Full static FAQ/menu KB for every message — intent does not trim the knowledge base.
    """
    del intent  # kept for call-site compatibility
    text = await load_static_knowledge(tenant)
    if resolve_dynamic_data_s3_key(tenant) and resolve_dynamic_data_kind(tenant) != "none":
        text = strip_embedded_data_blocks(text)
    return text
