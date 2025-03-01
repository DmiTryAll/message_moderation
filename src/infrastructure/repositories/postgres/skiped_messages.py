from typing import Iterable
from sqlalchemy import select

from domain.entity.skiped_message import SkipedMessage
from domain.repositories.skiped_messages import ABCSkipedMessagesRepository
from infrastructure.repositories.postgres.base import BasePosgresRepository
from infrastructure.repositories.postgres.models.skiped_message import SkipedMessageORM


class PosgresSkipedMessagesRepository(BasePosgresRepository, ABCSkipedMessagesRepository):
    
    async def check_exist(self, id: int) -> bool:
        stmt = select(SkipedMessageORM).where(SkipedMessageORM.id == id)
        result = await self.db_session.execute(stmt)
        return bool(result.scalar_one_or_none())

    async def save(self, skiped_message: SkipedMessage) -> int:
        skiped_message_orm = SkipedMessageORM(
            id=skiped_message.id,
        )
        self.db_session.add(skiped_message_orm)
        await self.db_session.flush()
        return skiped_message_orm.id
    
    async def add(self, skiped_messages: Iterable[SkipedMessage]) -> None:
        skiped_messages_orm = [
            SkipedMessageORM(
                id=sm.id,
            )
            for sm in skiped_messages
        ]
        self.db_session.add_all(skiped_messages_orm)
        await self.db_session.flush()
