import asyncio

from application.container import init_container
from domain.services.message_moderation import MessageModerationService
from infrastructure.repositories.postgres.database import Database


async def main():
    container = init_container()

    database: Database = container.resolve(Database)
    message_moderation: MessageModerationService = container.resolve(MessageModerationService)

    await database.create_tables()
    session = database.start_session()

    async with session.begin():
        await message_moderation.moderate()

        await session.commit()


if "__main__" == __name__:
    asyncio.run(main())