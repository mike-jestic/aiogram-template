from typing import Any, Awaitable, Callable, Dict

from aiogram.dispatcher.middlewares.base import BaseMiddleware

from ..utils.dispatcher import Dispatcher
from ..protocols.telegram_user_event import TelegramUserEvent


class ServicesDIMiddleware(BaseMiddleware):
    def __init__(self, dispatcher: Dispatcher):
        self.dispatcher = dispatcher

    async def __call__(
        self,
        handler: Callable[[TelegramUserEvent, Dict[str, Any]], Awaitable[Any]],
        event: TelegramUserEvent,
        data: Dict[str, Any],
    ) -> Any:
        
        data.update(self.dispatcher.services._services)
        return await handler(event, data)
