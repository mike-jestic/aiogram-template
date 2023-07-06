from typing import Any, Awaitable, Callable, Dict

from aiogram import Bot
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.dispatcher.middlewares.base import BaseMiddleware

from ..protocols.telegram_user_event import TelegramUserEvent
from aiogram.dispatcher.flags import get_flag


class DelMurkapMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramUserEvent, Dict[str, Any]], Awaitable[Any]],
        event: TelegramUserEvent,
        data: Dict[str, Any]
    ) -> Any:
        'example: dp.message(flags={"del_murkap": True})'

        msg = await handler(event, data)

        state: FSMContext = data.get('state', None)
        state_data = await state.get_data()

        if isinstance(msg, Message):
            await state.update_data(last_msg=msg)

        if get_flag(data, "del_murkap") and state_data.get('last_msg', None):
            await state_data['last_msg'].edit_reply_markup(reply_markup=None)

        return msg