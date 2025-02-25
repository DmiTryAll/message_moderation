from dataclasses import dataclass

from redis.asyncio import Redis

from domain.utils.progress_counter_storage import ProgressCounterStorage


@dataclass
class ProgressCounterRedisStorage(ProgressCounterStorage):
    client: Redis
    key: str = "progress_counter"

    async def get(self) -> int:
        result: bytes = await self.client.get(self.key)
        if not result:
            return 0
        return int(result.decode())

    async def set(self, value: int) -> None:
        await self.client.set(self.key, value)