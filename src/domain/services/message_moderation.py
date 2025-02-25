from dataclasses import dataclass
from typing import Iterable

from domain.exceptions.service import IgnoredMessageExistException
from domain.repositories.ignored_messages import ABCIgnoredMessagesRepository
from domain.repositories.messages import ABCMessagesRepository
from domain.entity.ignored_message import IgnoredMessage
from domain.utils.progress_counter_storage import ProgressCounterStorage
from domain.utils.skiped_message_ids_storage import SkipedMessageIdsStorage
from infrastructure.proxy.report_proxy import ABCReportProxy


@dataclass
class MessageModerationService:
    messages_repo: ABCMessagesRepository
    ignored_messages_repo: ABCIgnoredMessagesRepository
    progress_counter_storage: ProgressCounterStorage
    skiped_message_ids_storage: SkipedMessageIdsStorage
    report_proxy: ABCReportProxy
    num_records_per_req: int
    num_repetitions_for_report: int
    
    async def create_new_ignored_message(self, text: str) -> IgnoredMessage:
        if await self.ignored_messages_repo.check_exists(text.lower()):
            raise IgnoredMessageExistException
        ignored_message = IgnoredMessage.create(text=text.lower())
        ignored_message.id = await self.ignored_messages_repo.save(ignored_message)
        return ignored_message
    
    async def delete_ignored_message(self, text: str) -> None:
        await self.ignored_messages_repo.delete(text.lower())
    
    async def get_ignored_messages(self) -> Iterable[IgnoredMessage]:
        return await self.ignored_messages_repo.get_all()
    
    async def moderate(self) -> None:
        progress_counter = await self.progress_counter_storage.get()

        messages = await self.messages_repo.get_all(
            offset=progress_counter,
            limit=self.num_records_per_req
        )

        for indx, message in enumerate(messages):
            if await self.ignored_messages_repo.check_exists(message.text.lower()):
                continue

            if await self.skiped_message_ids_storage.is_exist(message.id):
                continue
            
            repeated_messages = await self.messages_repo.get_by_text_and_owner_id(
                text=message.text,
                owner_id=message.owner_id
            )

            filter_repeated_messages = []
            for repeated_message in repeated_messages:
                if not await self.skiped_message_ids_storage.is_exist(repeated_message.id):
                    filter_repeated_messages.append(repeated_message)

            if len(filter_repeated_messages) < self.num_repetitions_for_report:
                continue
            
            repeated_message_ids = [m.id for m in filter_repeated_messages]
            await self.skiped_message_ids_storage.add(repeated_message_ids)

            if not await self.report_proxy.report(message.text, message.owner_id):
                break

        await self.progress_counter_storage.set(
            progress_counter + indx
        )

