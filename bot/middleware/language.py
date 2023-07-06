from typing import Any, Awaitable, Callable, Dict

from aiogram.types import TelegramObject
from aiogram.utils.i18n import I18n, SimpleI18nMiddleware


class LanguageMiddleware(SimpleI18nMiddleware):
    def __init__(self, i18n: I18n):
        super().__init__(i18n, '_')

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        current_locale = await self.get_locale(event=event, data=data) or self.i18n.default_locale
        # current_locale = 'en'
        
        if self.i18n_key:
            data[self.i18n_key] = self.i18n.gettext
        if self.middleware_key:
            data[self.middleware_key] = self

        with self.i18n.context(), self.i18n.use_locale(current_locale):
            return await handler(event, data)
        