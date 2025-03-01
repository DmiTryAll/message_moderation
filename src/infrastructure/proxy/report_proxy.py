from abc import ABC
from dataclasses import dataclass

from aiogram import Bot


class ABCReportProxy(ABC):
     
    async def report(self, text: str, owner_id: int) -> bool:
        ...


@dataclass
class ReportProxy(ABCReportProxy):
    bot: Bot
    chat_id: int

    async def report(self, text: str, owner_id: int) -> bool:
        await self.bot.send_message(
            chat_id=self.chat_id,
            text=f"Повторяющееся сообщение:\n\n{text}\n\nОт пользователя: {owner_id}"
        )
        return True