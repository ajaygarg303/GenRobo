"""Tenant access checks and monthly session usage (Phase 1 billing foundation)."""

from __future__ import annotations

from datetime import datetime, timezone

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Plan, Tenant, TenantUsageMonthly

CHAT_ENABLED_STATUSES = frozenset({"active", "trial"})


def current_year_month() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m")


def assert_tenant_chat_available(tenant: Tenant) -> None:
    if tenant.status not in CHAT_ENABLED_STATUSES:
        raise HTTPException(
            status_code=403,
            detail="This business chat is not available right now.",
        )
    if tenant.status == "cancelled" and tenant.subscription_ends_at:
        now = datetime.now(timezone.utc)
        ends = tenant.subscription_ends_at
        if ends.tzinfo is None:
            ends = ends.replace(tzinfo=timezone.utc)
        if now > ends:
            raise HTTPException(
                status_code=403,
                detail="This business chat is not available right now.",
            )


async def get_plan_for_tenant(session: AsyncSession, tenant: Tenant) -> Plan | None:
    if not tenant.plan_id:
        return None
    r = await session.execute(select(Plan).where(Plan.id == tenant.plan_id))
    return r.scalar_one_or_none()


async def get_or_create_usage(
    session: AsyncSession, tenant_id, year_month: str | None = None
) -> TenantUsageMonthly:
    ym = year_month or current_year_month()
    r = await session.execute(
        select(TenantUsageMonthly).where(
            TenantUsageMonthly.tenant_id == tenant_id,
            TenantUsageMonthly.year_month == ym,
        )
    )
    row = r.scalar_one_or_none()
    if row:
        return row
    row = TenantUsageMonthly(tenant_id=tenant_id, year_month=ym, session_count=0)
    session.add(row)
    await session.flush()
    return row


async def assert_session_quota(session: AsyncSession, tenant: Tenant) -> None:
    plan = await get_plan_for_tenant(session, tenant)
    if not plan:
        return
    usage = await get_or_create_usage(session, tenant.id)
    if usage.session_count >= plan.max_sessions_per_month:
        raise HTTPException(
            status_code=429,
            detail="Monthly chat session limit reached for this business.",
        )


async def increment_session_usage(session: AsyncSession, tenant: Tenant) -> None:
    usage = await get_or_create_usage(session, tenant.id)
    usage.session_count += 1
    await session.flush()
