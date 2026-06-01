"""Siyu Tech: uses shared dynamic inventory_csv enrichment (retail_electronics)."""

from __future__ import annotations

from app.models import Tenant
from app.services.intent import ChatIntent, IntentResult
from app.services.structured.dynamic_data import enrich_from_dynamic_data


class SiyuCustomizer:
    async def enrich(
        self,
        tenant: Tenant,
        user_text: str,
        intent: ChatIntent,
        knowledge: str,
        intent_result: IntentResult | None = None,
    ) -> str | None:
        if intent_result is None:
            return None
        return await enrich_from_dynamic_data(tenant, user_text, intent, intent_result)
