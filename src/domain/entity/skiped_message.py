from dataclasses import dataclass

from domain.entity.base import BaseEntity


@dataclass(kw_only=True)
class SkipedMessage(BaseEntity):
    id: int