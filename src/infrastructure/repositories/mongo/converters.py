from typing import Any, Mapping

from domain.entity.chat import Chat
from domain.entity.message import Message


def convert_message_document_to_entity(message_document: Mapping[str, Any]) -> Message:
    return Message(
        message_id=message_document["message_id"],
        owner_card_id=message_document["owner_card_id"],
        text=message_document["text"],
        created_at=message_document["created_at"],
        message_type=message_document["message_type"],
        has_been_read_at=message_document["has_been_read_at"],
    )


def convert_aggregate_message_document_to_entity(chat_with_message_document: Mapping[str, Any]) -> Message:
    return convert_message_document_to_entity(chat_with_message_document["messages"])


def convert_chat_document_to_entity(chat_document: Mapping[str, Any]) -> Chat:
    return Chat(
        participants=chat_document["participants"],
        messages=[
            convert_message_document_to_entity(message) for message in chat_document["messages"]
        ],
        created_at=chat_document["created_at"],
    )