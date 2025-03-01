from abc import ABC
from typing import Iterable

from domain.entity.skiped_message import SkipedMessage


class ABCSkipedMessagesRepository(ABC):

    async def check_exist(self, id: int) -> bool:
        ...
    
    async def save(self, skiped_message: SkipedMessage) -> None:
        ...

    async def add(self, skiped_messages: Iterable[SkipedMessage]) -> None:
        ...
