"""Load tenant knowledge from S3 with optional Redis cache; RDS faq_text as fallback."""

from __future__ import annotations

import asyncio
import logging
import re

import boto3
from botocore.exceptions import ClientError

from app.config import get_settings
from app.models import Tenant

logger = logging.getLogger(__name__)

_MAX_KB_BYTES = 500_000

_redis_client = None

_CSV_BLOCK_RE = re.compile(
    r"## Product availability.*?(?=\n## |\Z)|```csv\s*\n.*?```",
    re.DOTALL | re.IGNORECASE,
)


async def init_knowledge_redis() -> None:
    global _redis_client
    url = get_settings().redis_url.strip()
    if not url:
        return
    try:
        import redis.asyncio as redis

        _redis_client = redis.from_url(url, decode_responses=True)
        await _redis_client.ping()
        logger.info("Redis KB cache enabled")
    except Exception as e:
        _redis_client = None
        logger.warning("Redis unavailable for KB cache (continuing without cache): %s", e)


async def close_knowledge_redis() -> None:
    global _redis_client
    if _redis_client is not None:
        await _redis_client.aclose()
        _redis_client = None


def strip_embedded_data_blocks(text: str) -> str:
    """Remove merged inventory CSV sections from static FAQ when dynamic file is separate."""
    if not text:
        return text
    cleaned = _CSV_BLOCK_RE.sub("", text)
    return re.sub(r"\n{3,}", "\n\n", cleaned).strip()


def _fetch_s3_object_text(bucket: str, key: str) -> str:
    client = boto3.client("s3")
    obj = client.get_object(Bucket=bucket, Key=key)
    raw = obj["Body"].read(_MAX_KB_BYTES + 1)
    if len(raw) > _MAX_KB_BYTES:
        logger.warning("S3 object truncated at %s bytes: s3://%s/%s", _MAX_KB_BYTES, bucket, key)
        raw = raw[:_MAX_KB_BYTES]
    return raw.decode("utf-8", errors="replace")


async def load_s3_text(
    tenant_id,
    s3_key: str,
    *,
    cache_suffix: str,
    fallback: str = "",
) -> str:
    """Load one S3 object with optional Redis cache (cache key kb:{suffix}:{tenant_id})."""
    key = (s3_key or "").strip()
    bucket = get_settings().knowledge_s3_bucket.strip()
    if not key or not bucket:
        return fallback

    cache_key = f"kb:{cache_suffix}:{tenant_id}"
    if _redis_client is not None:
        try:
            cached = await _redis_client.get(cache_key)
            if cached is not None:
                return cached if cached.strip() else fallback
        except Exception as e:
            logger.warning("Redis GET failed for %s: %s", cache_key, e)

    try:
        body = await asyncio.to_thread(_fetch_s3_object_text, bucket, key)
    except ClientError as e:
        code = (e.response.get("Error") or {}).get("Code", "")
        logger.warning("S3 read failed for s3://%s/%s (%s)", bucket, key, code)
        return fallback
    except Exception as e:
        logger.warning("S3 read failed for s3://%s/%s: %s", bucket, key, e)
        return fallback

    text = body.strip()
    if not text:
        return fallback

    ttl = max(60, int(get_settings().kb_cache_ttl_seconds))
    if _redis_client is not None:
        try:
            await _redis_client.set(cache_key, text, ex=ttl)
        except Exception as e:
            logger.warning("Redis SET failed for %s: %s", cache_key, e)

    return text


async def load_static_knowledge(tenant: Tenant) -> str:
    """
    Static FAQ / menu knowledge (knowledge_s3_key or faq_text).
    Does not load dynamic inventory/slots files.
    """
    faq = (tenant.faq_text or "").strip()
    s3_key = (tenant.knowledge_s3_key or "").strip()
    if s3_key:
        text = await load_s3_text(
            tenant.id,
            s3_key,
            cache_suffix="static",
            fallback=faq or "(No FAQ text uploaded yet.)",
        )
        return text
    return faq or "(No FAQ text uploaded yet.)"


async def load_tenant_knowledge(tenant: Tenant) -> str:
    """Backward-compatible alias for static KB only."""
    return await load_static_knowledge(tenant)


async def invalidate_tenant_kb_cache(tenant_id) -> None:
    if _redis_client is None:
        return
    for suffix in ("static", "dynamic"):
        try:
            await _redis_client.delete(f"kb:{suffix}:{tenant_id}")
        except Exception as e:
            logger.warning("Redis DEL failed for kb:%s:%s: %s", suffix, tenant_id, e)

    # legacy key from older deploys
    try:
        await _redis_client.delete(f"kb:{tenant_id}")
    except Exception:
        pass
