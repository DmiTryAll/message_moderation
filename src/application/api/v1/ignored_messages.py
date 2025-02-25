from typing import Annotated

from fastapi import Depends, status
from fastapi.exceptions import HTTPException
from fastapi.routing import APIRouter

from application.api.utils.depends import get_message_moderation_service
from application.api.v1.schemas import (
    CreateIgnoredMessageRequestSchema,
    CreateIgnoredMessageResponseSchema,
    DeleteIgnoredMessageRequestSchema,
    DeleteIgnoredMessageResponseSchema,
    ErrorSchema,
    GetAllIgnoredMessagesResponseSchema,
)
from domain.exceptions.base import DomainException
from domain.services.message_moderation import MessageModerationService


ignored_messages_router = APIRouter(
    tags=["IgnoredMessages"],
)


@ignored_messages_router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    description="Эндпоинт для создания нового игнорируемого сообщения",
    responses={
        status.HTTP_201_CREATED: {"model": CreateIgnoredMessageResponseSchema},
        status.HTTP_409_CONFLICT: {"model": ErrorSchema},
    },
)
async def create_ignored_message_handler(
    schema: CreateIgnoredMessageRequestSchema,
    message_moderation_service: Annotated[MessageModerationService, Depends(get_message_moderation_service)]
) -> CreateIgnoredMessageResponseSchema:
    try:
        ignored_message = await message_moderation_service.create_new_ignored_message(schema.text)        
    except DomainException as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": exception.message}
        )

    return CreateIgnoredMessageResponseSchema.from_entity(ignored_message)


@ignored_messages_router.delete(
    "/",
    status_code=status.HTTP_202_ACCEPTED,
    description="Эндпоинт для удаления игнорируемого сообщения",
    responses={
        status.HTTP_202_ACCEPTED: {"model": DeleteIgnoredMessageResponseSchema},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorSchema},
    },
)
async def delete_ignored_message_handler(
    schema: DeleteIgnoredMessageRequestSchema,
    message_moderation_service: Annotated[MessageModerationService, Depends(get_message_moderation_service)]
) -> DeleteIgnoredMessageResponseSchema:
    try:
        await message_moderation_service.delete_ignored_message(schema.text)        
    except DomainException as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": exception.message}
        )

    return DeleteIgnoredMessageResponseSchema(success=True)


@ignored_messages_router.get(
    "/",
    status_code=status.HTTP_200_OK,
    description="Эндпоинт получения всех игнорируемых сообщений",
    responses={
        status.HTTP_200_OK: {"model": GetAllIgnoredMessagesResponseSchema},
        status.HTTP_404_NOT_FOUND: {"model": ErrorSchema},
    },
)
async def get_all_ignored_messages_handler(
    message_moderation_service: Annotated[MessageModerationService, Depends(get_message_moderation_service)]
) -> GetAllIgnoredMessagesResponseSchema:
    try:
        ignored_messages = await message_moderation_service.get_ignored_messages()        
    except DomainException as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": exception.message}
        )

    return GetAllIgnoredMessagesResponseSchema.from_entities(ignored_messages)