from typing import Self
from pydantic import BaseModel

from domain.entity.ignored_message import IgnoredMessage


class ErrorSchema(BaseModel):
    error: str


class IgnoredMessageSchema(BaseModel):
    id: str
    text: str

    @classmethod
    def from_entity(cls, entity: IgnoredMessage) -> Self:
        return cls(
            id=entity.id,
            text=entity.text
        )


class CreateIgnoredMessageRequestSchema(BaseModel):
    text: str


class CreateIgnoredMessageResponseSchema(IgnoredMessageSchema):
    pass


class DeleteIgnoredMessageRequestSchema(BaseModel):
    text: str


class DeleteIgnoredMessageResponseSchema(BaseModel):
    success: bool


class GetAllIgnoredMessagesResponseSchema(BaseModel):
    count: int
    items: list[IgnoredMessageSchema]

    @classmethod
    def from_entities(cls, entities: list[IgnoredMessage]) -> Self:
        return cls(
            count=len(entities),
            items=[IgnoredMessageSchema.from_entity(entity) for entity in entities]
        )