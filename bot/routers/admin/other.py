
from aiogram import F, Bot, types
from aiogram.utils.i18n import gettext as _

from ...callback_data import DeleteCallbackData
from ...services.database.models import BotUser
from ...services.database.models import Metric, BotUser

from . import router


@router.callback_query(DeleteCallbackData.filter())
async def actions_with_user(call: types.CallbackQuery, callback_data: DeleteCallbackData, bot: Bot):
    if callback_data.type_entity == 'metric':
        entity = await Metric.get_or_none(id=callback_data.id)

    elif callback_data.type_entity == 'user':
        entity = await BotUser.get_or_none(id=callback_data.id)
    
    elif callback_data.type_entity == 'back':
        return call.message.answer(_('❌ Действие отменено'))
    
    if not entity:
        return call.message.answer(_('❗️ Объект уже удален'))
    
    await entity.delete()

    await call.message.edit_text(_('✅ Успешно удалено'), reply_markup=markups.admin_panel())
