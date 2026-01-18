import asyncio
from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy import select

import app.infrastructure.config.database.persistence as models
from app.domain.ValueObjects import BillingCycle
from app.infrastructure.config.database.DatabaseSession import DatabaseSessionFactory
from app.infrastructure.config.EnvConfig import EnvConfig

config = EnvConfig.load()
db_factory = DatabaseSessionFactory(config.database)


async def seed_plans():
    async with db_factory.get_session() as session:
        existing_plans = await session.execute(select(models.PlanModel))
        if existing_plans.scalars().first():
            print("Plans already seeded. Skipping...")
            return

        plans = [
            models.PlanModel(
                id=uuid4(),
                name="Anonym",
                billing_cycle=BillingCycle.LIFETIME.value,
                features=[],
                rate_limits={"requests_per_second": 1, "burst": 2},
                quota_limits={"api_calls_per_day": 1},
                is_active=True,
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc)
            ),
            models.PlanModel(
                id=uuid4(),
                name="Free",
                billing_cycle=BillingCycle.MONTHLY.value,
                features=["basic_support", "email_auth"],
                rate_limits={"requests_per_second": 5, "burst": 10},
                quota_limits={"api_calls_per_day": 50},
                is_active=True,
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc)
            ),
            models.PlanModel(
                id=uuid4(),
                name="Pro",
                billing_cycle=BillingCycle.MONTHLY.value,
                features=["priority_support", "email_auth", "oauth2", "api_key", "analytics"],
                rate_limits={"requests_per_second": 20, "burst": 50},
                quota_limits={"api_calls_per_day": 1000},
                is_active=True,
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc)
            ),
            models.PlanModel(
                id=uuid4(),
                name="Enterprise",
                billing_cycle=BillingCycle.CUSTOM.value,
                features=["dedicated_support", "sla_99.9", "custom_integration", "webhooks"],
                rate_limits={"requests_per_second": 100, "burst": 200},
                quota_limits={"api_calls_per_day": -1},
                is_active=True,
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc)
            )
        ]

        for plan in plans:
            session.add(plan)

        print(f"Seeded {len(plans)} plans successfully!")


async def seed_services():
    async with db_factory.get_session() as session:
        existing_services = await session.execute(select(models.ServiceModel))
        if existing_services.scalars().first():
            print("Services already seeded. Skipping...")
            return

        services = [
            models.ServiceModel(
                id=uuid4(),
                name="cvmaker",
                display_name="CV Maker",
                description="Professional CV/Resume builder service",
                is_active=True,
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc)
            ),
            models.ServiceModel(
                id=uuid4(),
                name="jobportal",
                display_name="Job Portal",
                description="Job search and application management",
                is_active=True,
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc)
            ),
            models.ServiceModel(
                id=uuid4(),
                name="3dbinpacking",
                display_name="3D Bin Packing",
                description="3D bin packing optimization service",
                is_active=True,
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc)
            ),
            models.ServiceModel(
                id=uuid4(),
                name="media_information",
                display_name="Media Information",
                description="Media metadata and information service",
                is_active=True,
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc)
            )
        ]

        for service in services:
            session.add(service)

        print(f"Seeded {len(services)} services successfully!")


async def main():
    print("Starting database seeding...")
    await seed_plans()
    await seed_services()
    await db_factory.close()
    print("Database seeding completed successfully!")


if __name__ == "__main__":
    asyncio.run(main())
