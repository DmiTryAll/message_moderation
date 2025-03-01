from typing import Iterable
from sqlalchemy import select, delete as delete_

from domain.entity.ignored_message import IgnoredMessage
from domain.repositories.ignored_messages import ABCIgnoredMessagesRepository
from infrastructure.repositories.postgres.base import BasePosgresRepository
from infrastructure.repositories.postgres.models.ignored_message import IgnoredMessageORM


class PosgresIgnoredMessagesRepository(BasePosgresRepository, ABCIgnoredMessagesRepository):
    
    async def check_exists(self, text: str) -> bool:
        stmt = select(IgnoredMessageORM).where(IgnoredMessageORM.text == text)
        result = await self.db_session.execute(stmt)
        return bool(result.scalar_one_or_none())

    async def save(self, entity: IgnoredMessage) -> int:
        ignored_message_orm = IgnoredMessageORM(
            text=entity.text,
        )
        self.db_session.add(ignored_message_orm)
        await self.db_session.flush()
        return ignored_message_orm.id
    
    async def delete(self, text: str) -> None:
        stmt = delete_(IgnoredMessageORM).where(IgnoredMessageORM.text == text)
        await self.db_session.execute(stmt)

    async def get_all(self) -> Iterable[IgnoredMessage]:
        stmt = select(IgnoredMessageORM)
        result = await self.db_session.execute(stmt)
        orms = result.unique().scalars()
        return [orm.to_entity() for orm in orms]
