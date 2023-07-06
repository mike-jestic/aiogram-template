from aiogram.utils.callback_answer import CallbackAnswerMiddleware
from aiogram.utils.i18n import I18n

from .bot_user import BotUserMiddleware
from .unprocessed_update import UnprocessedUpdateMiddleware
from .services_di import ServicesDIMiddleware
from .check_banned import BannedMiddleware
from .metric_referor import MetricsMiddleware
from .language import LanguageMiddleware
from .throttling import ThrottlingMiddleware
from ..utils.dispatcher import Dispatcher
from .chat_action import ChatActionMiddleware
from .del_murkup import DelMurkapMiddleware

def setup(dp: Dispatcher):
    
    LanguageMiddleware(
        I18n(
            path='bot/locales',
            default_locale='ru'
        )
    ).setup(dp)

    throttling_middleware = ThrottlingMiddleware()
    dp.message.outer_middleware.register(throttling_middleware)
    dp.callback_query.outer_middleware.register(throttling_middleware)

    banned_middleware = BannedMiddleware()
    dp.message.outer_middleware.register(banned_middleware)
    dp.callback_query.outer_middleware.register(banned_middleware)
    
    dp.callback_query.middleware(CallbackAnswerMiddleware())

    dp.message.outer_middleware.register(MetricsMiddleware())

    bot_user_middleware = BotUserMiddleware()
    dp.message.outer_middleware.register(bot_user_middleware)
    dp.callback_query.outer_middleware.register(bot_user_middleware)

    unprocessed_msg_middleware = UnprocessedUpdateMiddleware()
    dp.message.outer_middleware.register(unprocessed_msg_middleware)
    dp.callback_query.outer_middleware.register(unprocessed_msg_middleware)

    chat_action_middleware = ChatActionMiddleware()
    dp.message.middleware.register(chat_action_middleware)
    dp.callback_query.middleware.register(chat_action_middleware)

    del_murk_middleware = DelMurkapMiddleware()
    dp.message.middleware.register(del_murk_middleware)
    dp.callback_query.middleware.register(del_murk_middleware)

    services_di_middleware = ServicesDIMiddleware(dp)
    dp.message.middleware.register(services_di_middleware)
    dp.callback_query.middleware.register(services_di_middleware)
