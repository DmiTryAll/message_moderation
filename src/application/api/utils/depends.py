from typing import Annotated

from fastapi import Depends

from punq import Container

from application.container import init_container
from domain.services.message_moderation import MessageModerationService


def get_message_moderation_service(container: Annotated[Container, Depends(init_container)]) -> MessageModerationService:
    return container.resolve(MessageModerationService)