from typing import Any, Awaitable, Callable, Dict

from aiogram import Bot, types
from aiogram.utils.i18n import gettext as _
from aiogram.dispatcher.middlewares.base import BaseMiddleware

from ..services.database.models import BotUser
from ..protocols.telegram_user_event import TelegramUserEvent


class BannedMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramUserEvent, Dict[str, Any]], Awaitable[Any]],
        event: TelegramUserEvent,
        data: Dict[str, Any],
    ) -> Any:
        user: types.User = data["event_from_user"]

        bot_user = await BotUser.get_or_none(id=user.id)

        if bot_user and bot_user.is_banned == True:
            bot: Bot = data['bot']
            return await bot.send_message(bot_user.id, _('<b>Ваш аккаунт заблокирован!</b>'))

        return await handler(event, data)
