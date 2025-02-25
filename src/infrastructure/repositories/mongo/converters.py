from typing import Any, Mapping

from domain.entity.message import Message


def convert_message_document_to_entity(message_document: Mapping[str, Any]) -> Message:
    return Message(
        id=message_document["id"],
        type=message_document["type"],
        owner_id=message_document["owner_id"],
        text=message_document["text"],
        created_at=message_document["created_at"],
    )