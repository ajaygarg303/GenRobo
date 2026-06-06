"""LLM-based intent classification (primary path when OpenAI is configured)."""

from __future__ import annotations

import json
import logging

from openai import AsyncOpenAI

from app.config import get_settings
from app.models import ChatMessage, Tenant
from app.services.intent import ChatIntent, IntentResult
from app.services.intent_profiles import resolve_business_type
from app.services.tenant_knowledge import resolve_dynamic_data_kind, resolve_dynamic_data_s3_key

logger = logging.getLogger(__name__)

# confidence >= this means classify_intent_llm produced the result
LLM_CONFIDENCE = 10

_VALID_INTENTS = {i.value for i in ChatIntent}


def _openai_client() -> AsyncOpenAI | None:
    s = get_settings()
    if not s.openai_api_key:
        return None
    kwargs: dict[str, str] = {"api_key": s.openai_api_key}
    if s.openai_base_url.strip():
        kwargs["base_url"] = s.openai_base_url.rstrip("/")
    return AsyncOpenAI(**kwargs)


def _format_history(history: list[ChatMessage], limit: int = 6) -> str:
    lines: list[str] = []
    for m in history[-limit:]:
        if m.role in ("user", "assistant"):
            lines.append(f"{m.role.upper()}: {m.content}")
    return "\n".join(lines) if lines else "(no prior messages)"


def _has_dynamic_inventory(tenant: Tenant) -> bool:
    return (
        resolve_dynamic_data_kind(tenant) == "inventory_csv"
        and bool(resolve_dynamic_data_s3_key(tenant))
    )


async def classify_intent_llm(
    tenant: Tenant,
    user_text: str,
    history: list[ChatMessage],
) -> IntentResult | None:
    """
    Classify using the model + conversation context. Returns None if OpenAI unavailable or on error.
    """
    client = _openai_client()
    if client is None:
        return None

    business_type = resolve_business_type(
        tenant.slug,
        getattr(tenant, "business_type", None),
    )
    has_inventory = _has_dynamic_inventory(tenant) and business_type in (
        "retail_electronics",
        "retail",
    )

    system = (
        "You route messages for a multi-tenant business chatbot. "
        "Respond with JSON only: "
        '{"intent":"general|stock_price|menu_order|hours_location|contact",'
        '"load_dynamic_data":boolean}. '
        "Use the conversation so far — not keywords in isolation.\n\n"
        "intent meanings:\n"
        "- general: services (e.g. repairs), policies, general FAQs, follow-ups\n"
        "- stock_price: specific product availability or price (retail)\n"
        "- menu_order: food menu, ordering, order totals (restaurant)\n"
        "- hours_location: opening hours, address, directions\n"
        "- contact: customer asks how to reach the business, OR shares their own name/phone/email "
        "after being asked in the opening message\n\n"
        "load_dynamic_data: true ONLY when the latest message needs a live inventory/stock file "
        f"({'enabled' if has_inventory else 'disabled'} for this business) — including price, "
        "stock, or product photo/picture requests. "
        "false for repairs, hours, contact details, or vague questions.\n"
        "Examples: 'do you repair phones' → general, load_dynamic_data false. "
        "'iPhone 17 256GB price' → stock_price, load_dynamic_data true. "
        "'show me a photo of the used iPhone 17' → stock_price, load_dynamic_data true."
    )

    user = (
        f"Business: {tenant.display_name}\n"
        f"Business type: {business_type}\n\n"
        f"Conversation:\n{_format_history(history)}\n\n"
        f"Latest customer message:\n{user_text.strip()}"
    )

    try:
        s = get_settings()
        resp = await client.chat.completions.create(
            model=s.openai_model,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            temperature=0,
            max_tokens=80,
            response_format={"type": "json_object"},
        )
        raw = (resp.choices[0].message.content or "").strip()
        data = json.loads(raw)
        intent_raw = str(data.get("intent") or "general").strip().lower()
        if intent_raw not in _VALID_INTENTS:
            intent_raw = "general"
        intent = ChatIntent(intent_raw)
        load_dynamic = bool(data.get("load_dynamic_data")) and has_inventory
        scores = {i: (LLM_CONFIDENCE if i == intent else 0) for i in ChatIntent}
        return IntentResult(
            intent=intent,
            confidence=LLM_CONFIDENCE,
            scores=scores,
            business_type=business_type,
            load_dynamic_data=load_dynamic,
        )
    except Exception as e:
        logger.warning("LLM intent classification failed for tenant %s: %s", tenant.slug, e)
        return None
