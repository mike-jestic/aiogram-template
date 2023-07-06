from cachetools import TTLCache
from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import Message, User
from aiogram.utils.i18n import gettext as _


class ThrottlingMiddleware(BaseMiddleware):
    throt = TTLCache(maxsize=10_000, ttl=1)

    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any],
    ) -> Any:
        user: User = data["event_from_user"]

        if user.id in self.throt:
            count = self.throt[user.id] + 1
            self.throt[user.id] = count

            if count == 3:
                return await data['bot'].send_message(user.id, _('Не спамьте!'))
            elif count > 2:
                return
        else:
            self.throt[user.id] = 0

        return await handler(event, data)
