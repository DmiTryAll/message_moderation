from abc import ABC
from typing import Iterable


class SkipedMessageIdsStorage(ABC):

    async def is_exist(self, id: int) -> bool:
        ...

    async def add(self, ids: Iterable[int]) -> None:
        ...
