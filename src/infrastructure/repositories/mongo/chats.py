from dataclasses import dataclass
import re
from typing import Iterable

from domain.entity.message import Message
from domain.repositories.chats import ABCChatsRepository
from infrastructure.repositories.mongo.base import BaseMongoDBRepository
from infrastructure.repositories.mongo.converters import convert_aggregate_message_document_to_entity


@dataclass
class MongoDBChatsRepository(BaseMongoDBRepository, ABCChatsRepository):

    async def get_messages_by_text_and_owner_id(self, text: str, owner_card_id: int) -> Iterable[Message]:
        regex = re.compile(f"^{re.escape(text)}$", re.IGNORECASE)
        pipeline = [
            {"$unwind": "$messages"},
            {
                "$match": {
                    "$and": [
                        {"messages.text": regex},
                        {"messages.owner_card_id": owner_card_id}
                    ]
                }
            },
        ]
        cursor = self._collection.aggregate(pipeline)

        return [
            convert_aggregate_message_document_to_entity(chat_document)
            async for chat_document in cursor
        ]
    
    async def get_messages_ordered_by_created_at(self, offset: int = 0, limit: int = 50) -> Iterable[Message]:
        pipeline = [
            {"$unwind": "$messages"},
            {
                "$sort": {
                    "messages.created_at": 1
                }
            },
            {"$skip": offset},
            {"$limit": limit}
        ]

        cursor = self._collection.aggregate(pipeline)

        return [
            convert_aggregate_message_document_to_entity(chat_document)
            async for chat_document in cursor
        ]