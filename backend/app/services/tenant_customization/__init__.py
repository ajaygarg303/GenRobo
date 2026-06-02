"""Registry of per-tenant customization hooks."""

from __future__ import annotations

from app.models import Tenant
from app.services.intent import ChatIntent, IntentResult, classify_intent
from app.services.intent_profiles import get_profile
from app.services.structured.dynamic_data import enrich_from_dynamic_data
from app.services.tenant_customization.base import TenantCustomizer
from app.services.tenant_customization.india_gate import IndiaGateCustomizer

_REGISTRY: dict[str, TenantCustomizer] = {
    "india-gate": IndiaGateCustomizer(),
}

_RETAIL_TYPES = frozenset({"retail_electronics", "retail"})


async def enrich_for_tenant(
    tenant: Tenant,
    user_text: str,
    intent: ChatIntent | None,
    knowledge: str,
    intent_result: IntentResult | None = None,
) -> tuple[ChatIntent, str | None]:
    """
    Classify intent (if needed), load dynamic data when appropriate, apply tenant hooks.
    """
    resolved_result = intent_result or classify_intent(user_text, tenant)
    resolved = intent or resolved_result.intent

    if resolved_result.business_type in _RETAIL_TYPES:
        block = await enrich_from_dynamic_data(tenant, user_text, resolved, resolved_result)
        if block:
            return resolved, block

    customizer = _REGISTRY.get(tenant.slug)
    if customizer is None:
        return resolved, None

    block = await customizer.enrich(
        tenant, user_text, resolved, knowledge, intent_result=resolved_result
    )
    return resolved, block
