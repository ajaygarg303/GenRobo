"""Load tenant knowledge base from S3 with optional Redis cache; RDS faq_text as fallback."""

from __future__ import annotations

import asyncio
import logging

import boto3
from botocore.exceptions import ClientError

from app.config import get_settings
from app.models import Tenant

logger = logging.getLogger(__name__)

_MAX_KB_BYTES = 500_000

_redis_client = None


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


def _kb_cache_key(tenant_id) -> str:
    return f"kb:{tenant_id}"


def _fetch_s3_object_text(bucket: str, key: str) -> str:
    client = boto3.client("s3")
    obj = client.get_object(Bucket=bucket, Key=key)
    raw = obj["Body"].read(_MAX_KB_BYTES + 1)
    if len(raw) > _MAX_KB_BYTES:
        logger.warning("KB object truncated at %s bytes: s3://%s/%s", _MAX_KB_BYTES, bucket, key)
        raw = raw[:_MAX_KB_BYTES]
    return raw.decode("utf-8", errors="replace")


async def load_tenant_knowledge(tenant: Tenant) -> str:
    """
    Return KB text for the LLM system prompt.
    Order: Redis cache (hit) → S3 GetObject → faq_text fallback.
    """
    faq = (tenant.faq_text or "").strip()
    key = (tenant.knowledge_s3_key or "").strip()
    bucket = get_settings().knowledge_s3_bucket.strip()

    if not key or not bucket:
        return faq or "(No FAQ text uploaded yet.)"

    cache_key = _kb_cache_key(tenant.id)
    if _redis_client is not None:
        try:
            cached = await _redis_client.get(cache_key)
            if cached is not None:
                return cached if cached.strip() else (faq or "(No FAQ text uploaded yet.)")
        except Exception as e:
            logger.warning("Redis GET failed for %s: %s", cache_key, e)

    try:
        body = await asyncio.to_thread(_fetch_s3_object_text, bucket, key)
    except ClientError as e:
        code = (e.response.get("Error") or {}).get("Code", "")
        logger.warning("S3 KB read failed for s3://%s/%s (%s); using DB faq_text fallback", bucket, key, code)
        return faq or "(No FAQ text uploaded yet.)"
    except Exception as e:
        logger.warning("S3 KB read failed for s3://%s/%s: %s; using DB faq_text fallback", bucket, key, e)
        return faq or "(No FAQ text uploaded yet.)"

    text = body.strip()
    if not text:
        return faq or "(No FAQ text uploaded yet.)"

    ttl = max(60, int(get_settings().kb_cache_ttl_seconds))
    if _redis_client is not None:
        try:
            await _redis_client.set(cache_key, text, ex=ttl)
        except Exception as e:
            logger.warning("Redis SET failed for %s: %s", cache_key, e)

    return text


async def invalidate_tenant_kb_cache(tenant_id) -> None:
    """Clear cached KB after publishing a new object (optional; TTL still expires naturally)."""
    if _redis_client is None:
        return
    try:
        await _redis_client.delete(_kb_cache_key(tenant_id))
    except Exception as e:
        logger.warning("Redis DEL failed for kb:%s: %s", tenant_id, e)
