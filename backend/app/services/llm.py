from openai import AsyncOpenAI

from app.config import get_settings
from app.models import ChatMessage, Tenant
from app.services.fast_reply import try_fast_reply
from app.services.intent import ChatIntent, classify_intent_for_message
from app.services.tenant_customization import enrich_for_tenant
from app.services.product_images import append_inventory_photos
from app.services.tenant_knowledge import load_static_for_intent

_openai_client: AsyncOpenAI | None = None


def _client() -> AsyncOpenAI | None:
    global _openai_client
    s = get_settings()
    if not s.openai_api_key:
        return None
    if _openai_client is None:
        kwargs: dict[str, str] = {"api_key": s.openai_api_key}
        if s.openai_base_url.strip():
            kwargs["base_url"] = s.openai_base_url.rstrip("/")
        _openai_client = AsyncOpenAI(**kwargs)
    return _openai_client


def _intent_hint(intent: ChatIntent) -> str:
    hints = {
        ChatIntent.STOCK_PRICE: (
            "The customer is asking about product availability, price, or photos. "
            "Use structured lookup data when provided. Mention PHOTO lines when listing a SKU that has one."
        ),
        ChatIntent.MENU_ORDER: "The customer is asking about menu items or order totals. Use the static menu knowledge. Show itemised prices and a total.",
        ChatIntent.HOURS_LOCATION: "The customer is asking about opening hours or location.",
        ChatIntent.CONTACT: (
            "Use conversation context. If they are giving their own name/phone/email after your opening message, "
            "thank them and continue helping. Only share the business phone/email when they ask how to reach staff."
        ),
        ChatIntent.GENERAL: (
            "Answer helpfully using the static business knowledge — including services the business offers "
            "(repairs, delivery, appointments). Confirm yes/no from the KB before suggesting the customer call. "
            "Only defer to the team when the KB truly lacks the answer."
        ),
    }
    return hints.get(intent, hints[ChatIntent.GENERAL])


async def _build_system_prompt(
    tenant: Tenant,
    knowledge: str,
    intent: ChatIntent,
    enrichment: str | None,
    business_type: str,
) -> str:
    parts = [
        f"You are the website chat assistant for {tenant.display_name}.",
        "Answer using the business information below. If something is not covered, say you will pass the question to the team — do not invent prices, policies, or medical/legal advice.",
        "Product image URLs from lookup data may be shown as thumbnails — only use image_url values from dynamic data, never invent URLs.",
        (
            "Your opening message is the first turn in the conversation history. Read it carefully: "
            "if it asked for name or contact details and the customer replies with them, thank them briefly "
            "and invite their question — do not redirect them to call the business unless they ask how to reach staff."
        ),
        f"Business type: {business_type}. Routing hint: {intent.value} — {_intent_hint(intent)}",
        f"Business hours and notes: {tenant.business_hours_text or 'Not specified.'}",
        f"Public contact: phone={tenant.contact_phone or 'n/a'}, email={tenant.contact_email_public or 'n/a'}.",
        "--- Static knowledge (FAQ / menu — policies, services, how to order) ---",
        knowledge,
    ]
    if enrichment:
        parts.extend(
            [
                "--- Dynamic data for this message (stock, slots — authoritative when present) ---",
                enrichment,
            ]
        )
    return "\n\n".join(parts)


async def generate_reply(
    tenant: Tenant,
    history: list[ChatMessage],
    user_text: str,
) -> str:
    intent_result = await classify_intent_for_message(tenant, user_text, history)

    fast = try_fast_reply(tenant, user_text, conversation_started=bool(history))
    if fast is not None:
        return fast

    intent = intent_result.intent
    knowledge = await load_static_for_intent(tenant, intent)
    intent, enrichment = await enrich_for_tenant(
        tenant,
        user_text,
        intent,
        knowledge,
        intent_result=intent_result,
        history=history,
    )

    system = await _build_system_prompt(
        tenant, knowledge, intent, enrichment, intent_result.business_type
    )

    client = _client()
    messages: list[dict[str, str]] = [{"role": "system", "content": system}]
    for m in history:
        if m.role not in ("user", "assistant"):
            continue
        messages.append({"role": m.role, "content": m.content})
    messages.append({"role": "user", "content": user_text.strip()})

    if client is None:
        mock_extra = ""
        if enrichment:
            mock_extra = f"\n\n[Dynamic lookup]\n{enrichment[:400]}"
        return (
            "[Mock mode] OpenAI is not configured. "
            "Set OPENAI_API_KEY (and optionally OPENAI_MODEL, OPENAI_BASE_URL). "
            f"Intent={intent.value}. You asked: {user_text[:200]}{mock_extra}"
        )

    s = get_settings()
    max_tokens = 400 if intent in (ChatIntent.HOURS_LOCATION, ChatIntent.CONTACT) else 800
    resp = await client.chat.completions.create(
        model=s.openai_model,
        messages=messages,
        temperature=0.4,
        max_tokens=max_tokens,
    )
    choice = resp.choices[0].message.content
    text = (choice or "").strip() or "Sorry, I could not generate a reply."
    return append_inventory_photos(user_text, enrichment, text)
