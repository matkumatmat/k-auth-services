import asyncio

import app.infrastructure.config.database.persistence as models
from app.infrastructure.config.database.DatabaseSession import DatabaseSessionFactory
from app.infrastructure.config.EnvConfig import EnvConfig

config = EnvConfig.load()


async def create_tables():
    print("Creating database tables...")

    db_factory = DatabaseSessionFactory(config.database)

    async with db_factory._engine.begin() as conn:
        await conn.run_sync(models.BaseModel.metadata.create_all)

    await db_factory.close()
    print("All tables created successfully!")


if __name__ == "__main__":
    asyncio.run(create_tables())
