from aiogram import types
from aiogram.utils.i18n import gettext as _
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

from .services.database.models import BotUser
from .callback_data import ActionsWithUser, DeleteCallbackData


remove_markup = types.ReplyKeyboardRemove(remove_keyboard=True)

def admin_panel():
    return (
        InlineKeyboardBuilder()
        .button(text=_('📨 Рассылка'), callback_data='admin_mailing')
        .button(text=_('📈 Статистика'), callback_data='admin_statistics')
        .button(text=_('👤 Пользователи'), callback_data='admin_get_user')
        .adjust(2, repeat=True)
        .as_markup()
    )

def actions_with_user(user: BotUser):
    symbols = ['❌', '✅']
    markup = (
        InlineKeyboardBuilder()
        .button(text=_('{} Админ').format(symbols[user.admin]), callback_data=ActionsWithUser(user_id=user.id, action='admin').pack())
        .button(text=_('{} Забанен').format(symbols[user.is_banned]), callback_data=ActionsWithUser(user_id=user.id, action='ban').pack())
        .button(text=_('🗑 Удалить с базы'), callback_data=ActionsWithUser(user_id=user.id, action='del').pack())
        .button(text=_('◀️ Назад'), callback_data='back_admin')
        .adjust(2, repeat=True)
        .as_markup()
    )
    return markup

def question_delete_entity(entity_id: int, type_entity: str):
    markup = (
    InlineKeyboardBuilder()
        .button(text=f'✅', callback_data=DeleteCallbackData(id=entity_id, type_entity=type_entity).pack())
        .button(text=f'❌', callback_data=DeleteCallbackData(id=entity_id, type_entity='back').pack())
        .adjust(2, repeat=True)
        .as_markup()
    )
    return markup

def sending_keyboard():
    return (
        InlineKeyboardBuilder()
        .button(text=_('👥 Отправить всем'), callback_data='everyone')
        .button(text=_('👤 Отправить одному'), callback_data='one')
        .button(text=_('❌ Отменить'), callback_data='cancel')
        .adjust(2, repeat=True)
        .as_markup()
    )

def add_metric():
    return (
        InlineKeyboardBuilder()
        .button(text=_('➕ Добавить метрику'), callback_data='add_metric')
        .button(text=_('🗑 Удалить метрику'), callback_data='del_metric')
        .button(text=_('◀️ Назад'), callback_data='back_admin')
        .adjust(2, repeat=True)
        .as_markup()
    )

def back_admin():
    return (
        InlineKeyboardBuilder()
        .button(text=_('◀️ Назад'), callback_data='back_admin')
        .adjust(1, repeat=True)
        .as_markup()
    )

def example_reply():
    return (
        ReplyKeyboardBuilder()
        .button(text='First bnt')
        .button(text='Second bnt')
        .adjust(2, repeat=True)
        .as_markup(is_persistent=True, resize_keyboard=True)
    )
