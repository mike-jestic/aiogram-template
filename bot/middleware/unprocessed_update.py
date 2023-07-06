from typing import Callable, Dict, Any, Awaitable

from aiogram.utils.i18n import gettext as _
from aiogram import types, Bot, BaseMiddleware
from aiogram.dispatcher.event.bases import UNHANDLED


class UnprocessedUpdateMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[types.TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: types.update.Update,
        data: Dict[str, Any],
    ) -> Any:
        h = await handler(event, data)

        if h is UNHANDLED:
            bot: Bot = data['bot']
            from_user: types.User = event.from_user

            await bot.send_message(from_user.id, _('🙁 <i>Команда не найдена, введите /start</i>'))

        return h
