"""Load and search product inventory CSV (dynamic data file)."""

from __future__ import annotations

import csv
import io
import logging
import re

from app.models import Tenant
from app.services.knowledge import load_s3_text, strip_embedded_data_blocks
from app.services.knowledge import load_static_knowledge
from app.services.tenant_knowledge import resolve_dynamic_data_s3_key

logger = logging.getLogger(__name__)

_CSV_BLOCK_RE = re.compile(r"```csv\s*\n(.*?)```", re.DOTALL | re.IGNORECASE)


def parse_csv_text(text: str) -> list[dict[str, str]]:
    text = text.strip()
    if not text:
        return []
    reader = csv.DictReader(io.StringIO(text))
    if not reader.fieldnames:
        return []
    return [dict(row) for row in reader]


def _legacy_csv_from_static(tenant: Tenant) -> list[dict[str, str]]:
    """Fallback when dynamic file missing but old merged knowledge.md still has CSV."""
    import asyncio

    async def _load():
        static = await load_static_knowledge(tenant)
        match = _CSV_BLOCK_RE.search(static or "")
        if match:
            return parse_csv_text(match.group(1))
        return []

    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            return []
    except RuntimeError:
        pass
    return []


async def load_inventory_rows(tenant: Tenant) -> list[dict[str, str]]:
    """Load inventory from dynamic_data_s3_key; fallback to legacy CSV embedded in static KB."""
    key = resolve_dynamic_data_s3_key(tenant)
    if key:
        body = await load_s3_text(
            tenant.id,
            key,
            cache_suffix="dynamic",
            fallback="",
        )
        if body:
            rows = parse_csv_text(body)
            if rows:
                return rows

    static = await load_static_knowledge(tenant)
    match = _CSV_BLOCK_RE.search(static or "")
    if match:
        return parse_csv_text(match.group(1))
    return []


def _norm(s: str) -> str:
    return re.sub(r"\s+", " ", (s or "").lower()).strip()


def _tokens(text: str) -> set[str]:
    return {t for t in re.findall(r"[a-z0-9]+", _norm(text)) if len(t) >= 2}


def _row_search_blob(row: dict[str, str]) -> str:
    parts = [
        row.get("sku", ""),
        row.get("brand", ""),
        row.get("product_name", ""),
        row.get("category", ""),
        row.get("color", ""),
        row.get("storage_gb", ""),
        row.get("condition", ""),
    ]
    return _norm(" ".join(parts))


def search_inventory(
    rows: list[dict[str, str]],
    query: str,
    *,
    limit: int = 8,
) -> list[dict[str, str]]:
    if not rows or not query.strip():
        return []

    q_tokens = _tokens(query)
    if not q_tokens:
        return []

    scored: list[tuple[int, dict[str, str]]] = []
    for row in rows:
        blob = _row_search_blob(row)
        row_tokens = _tokens(blob)
        overlap = len(q_tokens & row_tokens)
        if overlap == 0:
            continue
        try:
            qty = int(str(row.get("stock_qty", "0")).strip() or "0")
        except ValueError:
            qty = 0
        score = overlap * 10 + (5 if qty > 0 else 0)
        for t in q_tokens:
            if t.isdigit() and t in blob:
                score += 3
        scored.append((score, row))

    scored.sort(key=lambda x: (-x[0], _row_search_blob(x[1])))
    return [row for _, row in scored[:limit]]


def format_inventory_matches(rows: list[dict[str, str]]) -> str:
    if not rows:
        return "No matching inventory rows found for this query."

    has_images = any((row.get("image_url") or "").strip() for row in rows)
    header = "sku | brand | product_name | color | storage_gb | condition | stock_qty | price_eur"
    if has_images:
        header += " | image_url"
    lines = [
        "Matching inventory (authoritative — use stock_qty and price_eur exactly):",
        header,
    ]
    if has_images:
        lines.append(
            "If the customer asks for a photo/picture, include the matching image_url on its own line "
            "(the chat UI renders it as a thumbnail)."
        )
    for row in rows:
        cols = [
            row.get("sku", ""),
            row.get("brand", ""),
            row.get("product_name", ""),
            row.get("color", ""),
            row.get("storage_gb", ""),
            row.get("condition", ""),
            row.get("stock_qty", ""),
            row.get("price_eur", ""),
        ]
        if has_images:
            cols.append((row.get("image_url") or "").strip())
        lines.append(" | ".join(cols))
    return "\n".join(lines)
