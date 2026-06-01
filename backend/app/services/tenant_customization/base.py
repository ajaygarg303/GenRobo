"""Per-tenant customization hooks (Phase 2b)."""

from __future__ import annotations

from typing import Protocol

from app.models import Tenant
from app.services.intent import ChatIntent, IntentResult


class TenantCustomizer(Protocol):
    async def enrich(
        self,
        tenant: Tenant,
        user_text: str,
        intent: ChatIntent,
        knowledge: str,
        intent_result: IntentResult | None = None,
    ) -> str | None:
        """Return extra system-prompt context for this turn, or None."""
