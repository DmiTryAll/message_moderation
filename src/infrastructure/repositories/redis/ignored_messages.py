from dataclasses import dataclass
from hashlib import sha512
from typing import Iterable

from domain.entity.ignored_message import IgnoredMessage
from domain.repositories.ignored_messages import ABCIgnoredMessagesRepository
from infrastructure.repositories.redis.base import BaseRedisRepository


@dataclass
class RedisIgnoredMessagesRepository(BaseRedisRepository, ABCIgnoredMessagesRepository):

    def __get_id(self, text: str) -> str:
        return sha512(text.encode()).hexdigest()
    
    def __get_key(self, text: str) -> str:
        return self.get_key(self.__get_id(text))
    
    async def check_exists(self, text: str) -> bool:
        key = self.__get_key(text)
        result = await self.client.exists(key)
        return bool(result)
    
    async def save(self, ignored_message: IgnoredMessage) -> str:
        id = self.__get_id(ignored_message.text)
        key = self.get_key(id)
        await self.client.set(key, ignored_message.text)
        return id
    
    async def delete(self, text: str) -> None:
        key = self.__get_key(text)
        await self.client.delete(key)

    async def get_all(self) -> Iterable[IgnoredMessage]:
        _, keys = await self.client.scan(match=self.get_key("*"))
        results = []
        for key in keys:
            _, id = key.decode().split(self.splitter)
            text = await self.client.get(key)
            results.append(
                IgnoredMessage(
                    id=id,
                    text=text.decode()
                )
            )
        return results
