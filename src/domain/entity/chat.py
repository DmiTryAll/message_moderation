from dataclasses import dataclass
from datetime import datetime

from domain.entity.base import BaseEntity
from domain.entity.message import Message


@dataclass(kw_only=True)
class Chat(BaseEntity):
    participants: list[int]
    messages: list[Message]
    created_at: datetime