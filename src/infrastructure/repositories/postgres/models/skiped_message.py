from typing import Self
from sqlalchemy.orm import Mapped, mapped_column

from domain.entity.skiped_message import SkipedMessage
from infrastructure.repositories.postgres.models.base import BaseORM


class SkipedMessageORM(BaseORM):
    __tablename__ = "skiped_message"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=False)

    @classmethod
    def from_entity(cls, entity: SkipedMessage) -> Self:
        return cls(
            id=entity.id,
        )

    def to_entity(self) -> SkipedMessage:
        return SkipedMessage(
            id=self.id,
        )