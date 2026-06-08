"""Load and enrich from tenant dynamic data files (by kind)."""

from __future__ import annotations

import logging

from app.models import ChatMessage, Tenant
from app.services.intent import ChatIntent
from app.services.structured.inventory_csv import (
    build_inventory_search_query,
    format_inventory_matches,
    load_inventory_rows,
    search_inventory,
)
from app.services.intent import IntentResult
from app.services.tenant_knowledge import resolve_dynamic_data_kind, should_load_dynamic_data

logger = logging.getLogger(__name__)


async def enrich_from_dynamic_data(
    tenant: Tenant,
    user_text: str,
    intent: ChatIntent,
    intent_result: IntentResult,
    history: list[ChatMessage] | None = None,
) -> str | None:
    """
    Structured lookup from dynamic_data_s3_key when intent allows.
    Returns text block for system prompt, or None.
    """
    if not should_load_dynamic_data(tenant, intent_result, user_text, history=history):
        return None

    kind = resolve_dynamic_data_kind(tenant)
    if kind == "inventory_csv":
        return await _enrich_inventory_csv(tenant, user_text, history=history)
    if kind == "appointment_slots":
        logger.info("appointment_slots dynamic kind not implemented yet for %s", tenant.slug)
        return None

    logger.warning("Unknown dynamic_data_kind=%s for tenant %s", kind, tenant.slug)
    return None


async def _enrich_inventory_csv(
    tenant: Tenant,
    user_text: str,
    *,
    history: list[ChatMessage] | None = None,
) -> str | None:
    rows = await load_inventory_rows(tenant)
    if not rows:
        from app.services.tenant_knowledge import resolve_dynamic_data_s3_key

        key = resolve_dynamic_data_s3_key(tenant)
        return (
            f"DYNAMIC STOCK FILE configured ({key}) but no rows loaded. "
            "Ask the customer to call the shop for availability."
        )

    search_query = build_inventory_search_query(user_text, history)
    matches = search_inventory(rows, search_query, limit=8)
    if not matches:
        return (
            "STOCK LOOKUP: no matching rows for this query. "
            "Ask for brand, model, storage (GB), and colour, or suggest calling the shop."
        )

    return "\n".join(
        [
            "STOCK LOOKUP (dynamic inventory file — use stock_qty and price_eur exactly):",
            format_inventory_matches(matches),
        ]
    )
