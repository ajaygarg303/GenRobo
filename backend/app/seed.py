import asyncio
import json
import uuid

from sqlalchemy import select

from app.db import SessionLocal, engine
from app.models import Base, Plan, Tenant

PLANS = [
    {
        "code": "basic",
        "display_name": "Basic",
        "max_sessions_per_month": 200,
        "entitlements": {"images": False, "appointments": False, "orders": False, "kb_suggestions": False},
    },
    {
        "code": "advanced",
        "display_name": "Advanced",
        "max_sessions_per_month": 2000,
        "entitlements": {"images": True, "appointments": False, "orders": False, "kb_suggestions": True},
    },
    {
        "code": "premium",
        "display_name": "Premium",
        "max_sessions_per_month": 20000,
        "entitlements": {"images": True, "appointments": True, "orders": True, "kb_suggestions": True},
    },
]


async def _ensure_plans(session) -> dict[str, Plan]:
    by_code: dict[str, Plan] = {}
    for spec in PLANS:
        r = await session.execute(select(Plan).where(Plan.code == spec["code"]))
        plan = r.scalar_one_or_none()
        if not plan:
            plan = Plan(
                id=uuid.uuid4(),
                code=spec["code"],
                display_name=spec["display_name"],
                max_sessions_per_month=spec["max_sessions_per_month"],
                entitlements_json=json.dumps(spec["entitlements"]),
            )
            session.add(plan)
        else:
            plan.display_name = spec["display_name"]
            plan.max_sessions_per_month = spec["max_sessions_per_month"]
            plan.entitlements_json = json.dumps(spec["entitlements"])
        by_code[spec["code"]] = plan
    await session.flush()
    return by_code


async def seed() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with SessionLocal() as session:
        plans = await _ensure_plans(session)

        r = await session.execute(select(Tenant).where(Tenant.slug == "demo"))
        demo = r.scalar_one_or_none()
        if not demo:
            demo = Tenant(
                id=uuid.uuid4(),
                slug="demo",
                display_name="Demo Plumbing Co.",
                timezone="Asia/Kolkata",
                status="active",
                plan_id=plans["basic"].id,
                primary_color="#0369a1",
                background_color="#f0f9ff",
                text_color="#0c4a6e",
                welcome_message="Hi! Ask us about services, rates, or hours.",
                faq_text=(
                    "Services: leak repair, drain cleaning, water heater install.\n"
                    "Rates: $95 service call (waived if work approved). "
                    "Emergency after 8pm: +$50.\n"
                    "Warranty: 90 days on labor for repairs we perform."
                ),
                business_hours_text="Mon–Sat 8am–6pm. Closed Sundays.",
                contact_phone="+1-555-0100",
                contact_email_public="hello@demoplumbing.example",
                transcript_email="owner@example.com",
            )
            session.add(demo)
            print("Seeded tenant slug=demo")
        else:
            if not demo.plan_id:
                demo.plan_id = plans["basic"].id
            if not getattr(demo, "status", None) or demo.status == "":
                demo.status = "active"

        await session.commit()


def main() -> None:
    asyncio.run(seed())


if __name__ == "__main__":
    main()
