from abc import ABC
from typing import Iterable

from domain.entity.ignored_message import IgnoredMessage


class ABCIgnoredMessagesRepository(ABC):

    async def check_exists(self, text: str) -> bool:
        ...
    
    async def save(self, ignored_message: IgnoredMessage) -> int:
        ...
    
    async def delete(self, text: str) -> None:
        ...

    async def get_all(self) -> Iterable[IgnoredMessage]:
        ...