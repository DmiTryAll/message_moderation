from dataclasses import dataclass

from domain.entity.base import BaseEntity


@dataclass(kw_only=True)
class IgnoredMessage(BaseEntity):
    id: str | None = None
    text: str

    @classmethod
    def create(cls, text: str) -> "IgnoredMessage":
        return cls(
            text=text
        )