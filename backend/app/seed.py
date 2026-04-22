import asyncio
import uuid

from sqlalchemy import select

from app.db import SessionLocal, engine
from app.models import Base, Tenant


async def seed() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with SessionLocal() as session:
        r = await session.execute(select(Tenant).where(Tenant.slug == "demo"))
        if r.scalar_one_or_none():
            return

        session.add(
            Tenant(
                id=uuid.uuid4(),
                slug="demo",
                display_name="Demo Plumbing Co.",
                timezone="Asia/Kolkata",
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
        )
        await session.commit()
        print("Seeded tenant slug=demo")


def main() -> None:
    asyncio.run(seed())


if __name__ == "__main__":
    main()
