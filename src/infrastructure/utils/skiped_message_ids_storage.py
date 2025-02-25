from dataclasses import dataclass
from typing import Iterable

from redis.asyncio import Redis

from domain.utils.skiped_message_ids_storage import SkipedMessageIdsStorage


@dataclass
class SkipedMessageIdsRedisStorage(SkipedMessageIdsStorage):
    client: Redis
    key: str = "skiped_message"

    def _get_key(self, id: int) -> str:
        return self.key + ":" + str(id)

    async def is_exist(self, id: int) -> bool:
        result = await self.client.exists(self._get_key(id))
        return bool(result)

    async def add(self, ids: Iterable[int]) -> None:
        for id in ids:
            await self.client.set(self._get_key(id), id)
