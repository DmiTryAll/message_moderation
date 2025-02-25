from abc import ABC


class ProgressCounterStorage(ABC):

    async def get(self) -> int:
        ...

    async def set(self, value: int) -> None:
        ...