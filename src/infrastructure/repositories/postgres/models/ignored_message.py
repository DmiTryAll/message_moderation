from typing import Self
import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from domain.entity.ignored_message import IgnoredMessage
from infrastructure.repositories.postgres.models.base import BaseORM


class IgnoredMessageORM(BaseORM):
    __tablename__ = "ignored_message"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    text: Mapped[str] = mapped_column(sa.Text(), nullable=False)

    @classmethod
    def from_entity(cls, entity: IgnoredMessage) -> Self:
        return cls(
            id=entity.id,
            text=entity.text,
        )

    def to_entity(self) -> IgnoredMessage:
        return IgnoredMessage(
            id=self.id,
            text=self.text,
        )