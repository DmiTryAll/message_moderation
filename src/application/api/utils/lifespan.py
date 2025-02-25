from application.container import init_container
from domain.services.message_moderation import MessageModerationService


async def moderate():
    container = init_container()

    message_moderation: MessageModerationService = container.resolve(MessageModerationService)

    while True:
        await message_moderation.moderate()