
from aiogram import F, types
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart

from .. import markups
from ..utils.router import Router
from . import root_handlers_router
from aiogram.utils.i18n import gettext as _
from ..services.database.models import BotUser


router = Router()
root_handlers_router.include_router(router)


@router.message(CommandStart())
async def start_handler(message: types.Message, state: FSMContext, bot_user: BotUser):
    await state.clear()
    await message.answer(_('Отлично! Бот запущен!'))
