import asyncio

from aiogram import exceptions
from aiogram.client.bot import Bot as AiogramBot

from ..models.config.bot_config import BotConfig


class Bot(AiogramBot):
    def __init__(self, config: BotConfig, *args, **kwargs):
        super().__init__(*args, token=config.bot_token, **kwargs)
        self.config = config

    async def __call__(self, *args, **kwargs):
        while True:
            try:
                return await super().__call__(*args, **kwargs)
            except exceptions.TelegramRetryAfter as e:
                await asyncio.sleep(e.retry_after)
