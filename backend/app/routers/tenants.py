from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_session
from app.models import Tenant
from app.schemas import TenantPublicConfig

router = APIRouter(prefix="/tenants", tags=["tenants"])


@router.get("/by-slug/{slug}", response_model=TenantPublicConfig)
async def get_tenant_public(slug: str, session: AsyncSession = Depends(get_session)) -> TenantPublicConfig:
    r = await session.execute(select(Tenant).where(Tenant.slug == slug))
    t = r.scalar_one_or_none()
    if not t:
        raise HTTPException(status_code=404, detail="Business not found")
    return TenantPublicConfig(
        slug=t.slug,
        display_name=t.display_name,
        timezone=t.timezone,
        primary_color=t.primary_color,
        background_color=t.background_color,
        text_color=t.text_color,
        logo_url=t.logo_url,
        welcome_message=t.welcome_message,
        business_hours_text=t.business_hours_text,
        contact_phone=t.contact_phone,
        contact_email_public=t.contact_email_public,
    )
