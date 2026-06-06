"""Append product image URLs to replies when inventory lookup provides them."""

from __future__ import annotations

import re

_PHOTO_ASK_RE = re.compile(
    r"\b(photo|photos|picture|pictures|pic|pics|image|images|show me|see it|look like)\b",
    re.IGNORECASE,
)


def _norm(s: str) -> str:
    return (s or "").strip()


def _parse_inventory_image_urls(enrichment: str) -> list[tuple[str, str]]:
    """Return (sku, https image_url) from STOCK LOOKUP enrichment text."""
    if not enrichment or "STOCK LOOKUP" not in enrichment:
        return []

    lines = enrichment.splitlines()
    header_idx = next(
        (i for i, ln in enumerate(lines) if "image_url" in ln.lower() and "|" in ln),
        None,
    )
    if header_idx is None:
        return []

    headers = [h.strip().lower() for h in lines[header_idx].split("|")]
    try:
        sku_i = headers.index("sku")
        url_i = headers.index("image_url")
    except ValueError:
        return []

    out: list[tuple[str, str]] = []
    for ln in lines[header_idx + 1 :]:
        if "|" not in ln or ln.strip().startswith("If the customer"):
            continue
        cols = [c.strip() for c in ln.split("|")]
        if len(cols) <= max(sku_i, url_i):
            continue
        sku = cols[sku_i]
        url = cols[url_i]
        if sku and url.lower().startswith(("http://", "https://")):
            out.append((sku, url))
    return out


def _urls_already_in_reply(reply: str, urls: list[str]) -> list[str]:
    missing = []
    low = reply.lower()
    for u in urls:
        if u.lower() not in low:
            missing.append(u)
    return missing


def append_inventory_photos(user_text: str, enrichment: str | None, reply: str) -> str:
    """
    Guarantee image URLs appear on their own lines when inventory has image_url,
    so the chat UI can render thumbnails (do not rely on the LLM alone).
    """
    if not enrichment:
        return reply

    pairs = _parse_inventory_image_urls(enrichment)
    if not pairs:
        return reply

    text = user_text or ""
    wants_photo = bool(_PHOTO_ASK_RE.search(text))
    text_low = text.lower()

    urls: list[str] = []
    if wants_photo:
        urls = [url for _, url in pairs]
    else:
        for sku, url in pairs:
            if sku.lower() in text_low or len(pairs) == 1:
                urls.append(url)

    urls = _urls_already_in_reply(reply, urls)
    if not urls:
        return reply

    # Cap thumbnails per message
    urls = urls[:3]
    return reply.rstrip() + "\n\n" + "\n".join(urls)
