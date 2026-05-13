from openai import AsyncOpenAI

from app.config import get_settings
from app.models import ChatMessage, Tenant
from app.services.knowledge import load_tenant_knowledge


def _client() -> AsyncOpenAI | None:
    s = get_settings()
    if not s.openai_api_key:
        return None
    kwargs: dict[str, str] = {"api_key": s.openai_api_key}
    if s.openai_base_url.strip():
        kwargs["base_url"] = s.openai_base_url.rstrip("/")
    return AsyncOpenAI(**kwargs)


async def _build_system_prompt(tenant: Tenant) -> str:
    knowledge = await load_tenant_knowledge(tenant)
    parts = [
        f"You are the website chat assistant for {tenant.display_name}.",
        "Answer using the business information below. If something is not covered, say you will pass the question to the team — do not invent prices, policies, or medical/legal advice.",
        f"Business hours and notes: {tenant.business_hours_text or 'Not specified.'}",
        f"Public contact: phone={tenant.contact_phone or 'n/a'}, email={tenant.contact_email_public or 'n/a'}.",
        "--- Business knowledge (FAQs, services, rates) ---",
        knowledge,
    ]
    return "\n\n".join(parts)


async def generate_reply(
    tenant: Tenant,
    history: list[ChatMessage],
    user_text: str,
) -> str:
    client = _client()
    system = await _build_system_prompt(tenant)
    messages: list[dict[str, str]] = [{"role": "system", "content": system}]
    for m in history:
        if m.role not in ("user", "assistant"):
            continue
        messages.append({"role": m.role, "content": m.content})
    messages.append({"role": "user", "content": user_text.strip()})

    if client is None:
        return (
            "[Mock mode] OpenAI is not configured. "
            "Set OPENAI_API_KEY (and optionally OPENAI_MODEL, OPENAI_BASE_URL). "
            f"You asked: {user_text[:200]}"
        )

    s = get_settings()
    resp = await client.chat.completions.create(
        model=s.openai_model,
        messages=messages,
        temperature=0.4,
        max_tokens=800,
    )
    choice = resp.choices[0].message.content
    return (choice or "").strip() or "Sorry, I could not generate a reply."
