from typing import Optional, Protocol

from aiogram import types


class TelegramUserEvent(Protocol):
    from_user: Optional[types.User]
