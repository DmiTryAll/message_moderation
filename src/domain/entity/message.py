from dataclasses import dataclass
import datetime

from domain.entity.base import BaseEntity


@dataclass(kw_only=True)
class Message(BaseEntity):
    id: int
    type: str
    owner_id: int
    text: str
    created_at: datetime