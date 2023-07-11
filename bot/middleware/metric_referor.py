from typing import Any, Awaitable, Callable, Dict

from aiogram.dispatcher.middlewares.base import BaseMiddleware

from ..services.database.models import BotUser, Metric
from ..protocols.telegram_user_event import TelegramUserEvent


class MetricsMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramUserEvent, Dict[str, Any]], Awaitable[Any]],
        event: TelegramUserEvent,
        data: Dict[str, Any],
    ) -> Any:
        if event.text:
            split = event.text.split()

            if split[0] == '/start' and len(split) == 2:
                bot_user = await BotUser.get_or_none(id=event.from_user.id)

                if not bot_user:
                    if split[1].isdecimal():
                        if referor := await BotUser.get_or_none(id=split[1]):
                            await BotUser.create(id=event.from_user.id, referrer=referor, username=event.from_user.username)
                    else:
                        if ads := await Metric.get_or_none(code=split[1]):
                            await BotUser.create(id=event.from_user.id, metric_id=ads.id, username=event.from_user.username)

        return await handler(event, data)
