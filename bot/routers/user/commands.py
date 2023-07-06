from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as _

from . import router
from ...services.database.models import BotUser
from ...filters.i18n_filter import TextFilter


@router.message(TextFilter('Проверка фильтра'))
async def get_my_reports(message: types.Message, state: FSMContext, bot_user: BotUser):
     await message.answer(_('Фильтр работает!'))
