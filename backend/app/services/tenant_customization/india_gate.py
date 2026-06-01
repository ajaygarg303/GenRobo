"""India Gate: menu/order rules (static menu KB; no dynamic file)."""

from __future__ import annotations

from app.models import Tenant
from app.services.intent import ChatIntent, IntentResult


class IndiaGateCustomizer:
    async def enrich(
        self,
        tenant: Tenant,
        user_text: str,
        intent: ChatIntent,
        knowledge: str,
        intent_result: IntentResult | None = None,
    ) -> str | None:
        if intent != ChatIntent.MENU_ORDER:
            return None

        return (
            "INDIA GATE ORDER RULES (apply for this message):\n"
            "- List each item with unit price from the static menu knowledge.\n"
            "- Curries items 17–31: price depends on protein — "
            "Chicken €12 · Lamb €13 · Vegetable €10 · Paneer €11 · Regular prawn €14. "
            "Ask which protein if not stated.\n"
            "- Starters marked Starter/Main: use the portion the customer asked for.\n"
            "- Add delivery €3.50 once if they want delivery (confirm if unclear).\n"
            "- Show line-by-line breakdown and grand total.\n"
            "- Do not invent prices; if missing, suggest calling 01 462 2704."
        )
