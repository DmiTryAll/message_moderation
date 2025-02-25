from abc import ABC
from dataclasses import dataclass

from redis.asyncio import Redis


@dataclass
class BaseRedisRepository(ABC):
    client: Redis
    prefix: str
    splitter: str = ":"

    def get_key(self, name: str) -> str:
        return self.splitter.join([self.prefix, name])
