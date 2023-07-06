from aiogram.types import Update
from aiogram.filters.base import Filter
from aiogram.utils.i18n import gettext as _

from ..protocols.telegram_user_event import TelegramUserEvent


class TextFilter(Filter):
    def __init__(self, text: str):
        self.text = text

    async def __call__(
        self,
        telegram_object: TelegramUserEvent,
        event_update: Update
    ) -> bool:
        return _(self.text) == event_update.message.text
