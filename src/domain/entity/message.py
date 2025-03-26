from dataclasses import dataclass
from datetime import datetime

from domain.entity.base import BaseEntity


@dataclass(kw_only=True)
class Message(BaseEntity):
    message_id: int
    owner_card_id: int
    text: str
    created_at: datetime
    message_type: str
    has_been_read_at: datetime