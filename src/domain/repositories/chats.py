from abc import ABC
from typing import Iterable

from domain.entity.message import Message


class ABCChatsRepository(ABC):
    
    async def get_messages_by_text_and_owner_id(self, text: str, owner_card_id: int) -> Iterable[Message]:
        ...
    
    async def get_messages_ordered_by_created_at(self, offset: int = 0, limit: int = 50) -> Iterable[Message]:
        ...