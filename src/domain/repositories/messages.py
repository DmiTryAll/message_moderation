from abc import ABC
from typing import Iterable

from domain.entity.message import Message


class ABCMessagesRepository(ABC):
    
    async def get_by_text_and_owner_id(self, text: str, owner_id: int) -> Iterable[Message]:
        ...
    
    async def get_all(self, offset: int = 0, limit: int = 50) -> Iterable[Message]:
        ...