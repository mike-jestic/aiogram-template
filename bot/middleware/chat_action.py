from typing import Any, Dict, Callable, Awaitable

from aiogram.dispatcher.flags import get_flag
from aiogram.types import TelegramObject, Message
from aiogram.utils.chat_action import ChatActionSender
from aiogram.dispatcher.middlewares.base import BaseMiddleware


class ChatActionMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        'example: dp.message(flags={"action_type": "upload_document"})'

        action_type = get_flag(data, "action_type")

        lst_action_type = [
            'typing', 'upload_photo', 'record_video',
            'upload_video', 'record_voice', 'upload_voice',
            'upload_document', 'choose_sticker', 'find_location',
            'record_video_note', 'upload_video_note'
        ]

        if not action_type or action_type not in lst_action_type:
            return await handler(event, data)
        
        async with ChatActionSender(
                action=action_type, 
                chat_id=event.chat.id
        ):
            return await handler(event, data)
        