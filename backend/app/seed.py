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
                display_name="Murphy's Corner Café (Demo)",
                timezone="Europe/Dublin",
                status="active",
                plan_id=plans["advanced"].id,
                business_type="restaurant",
                primary_color="#b45309",
                background_color="#fffbeb",
                text_color="#1c1917",
                welcome_message=(
                    "Welcome to the Murphy's Corner Café demo! Ask about our hours, menu, "
                    "delivery, or prices — answers come from our sample knowledge base only."
                ),
                knowledge_s3_key="tenants/demo/knowledge.md",
                faq_text="",
                business_hours_text="Mon–Sat 9am–9pm · Sun 10am–6pm",
                contact_phone="+353 1 555 0100",
                contact_email_public="hello@murphyscafe.demo",
                transcript_email="hello@myrobochat.com",
            )
            session.add(demo)
            print("Seeded tenant slug=demo")
        else:
            demo.display_name = "Murphy's Corner Café (Demo)"
            demo.timezone = "Europe/Dublin"
            demo.business_type = "restaurant"
            demo.plan_id = plans["advanced"].id
            demo.knowledge_s3_key = "tenants/demo/knowledge.md"
            demo.welcome_message = (
                "Welcome to the Murphy's Corner Café demo! Ask about our hours, menu, "
                "delivery, or prices — answers come from our sample knowledge base only."
            )
            demo.business_hours_text = "Mon–Sat 9am–9pm · Sun 10am–6pm"
            demo.contact_phone = "+353 1 555 0100"
            demo.contact_email_public = "hello@murphyscafe.demo"
            demo.transcript_email = "hello@myrobochat.com"
            demo.primary_color = "#b45309"
            demo.background_color = "#fffbeb"
            demo.text_color = "#1c1917"
            if not getattr(demo, "status", None) or demo.status == "":
                demo.status = "active"

        await session.commit()


def main() -> None:
    asyncio.run(seed())


if __name__ == "__main__":
    main()
