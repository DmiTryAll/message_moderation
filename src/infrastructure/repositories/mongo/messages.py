from dataclasses import dataclass
from typing import Iterable

from domain.entity.message import Message
from domain.repositories.messages import ABCMessagesRepository
from infrastructure.repositories.mongo.base import BaseMongoDBRepository
from infrastructure.repositories.mongo.converters import convert_message_document_to_entity


@dataclass
class MongoDBMessagesRepository(BaseMongoDBRepository, ABCMessagesRepository):

    async def get_by_text_and_owner_id(self, text: str, owner_id: int) -> Iterable[Message]:
        find = {
            "$and": [
                {"text": {"$regex": f"^{text}$", "$options": "i"}},
                {"owner_id": owner_id}
            ]
        }
        cursor = self._collection.find(find)

        return [
            convert_message_document_to_entity(message_document)
            async for message_document in cursor
        ]
    
    async def get_all(self, offset: int = 0, limit: int = 50) -> Iterable[Message]:
        cursor = self._collection.find().skip(offset).limit(limit)

        return [
            convert_message_document_to_entity(message_document)
            async for message_document in cursor
        ]