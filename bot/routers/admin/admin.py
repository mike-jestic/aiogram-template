from aiogram import F, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from aiogram.utils.i18n import gettext as _

from . import router
from ... import markups


@router.message(Command('admin'))
async def admin_panel(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer(_('👨‍💻 Админка'), reply_markup=markups.admin_panel())

@router.callback_query(F.data == 'back_admin')
async def back_admin(call: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await call.message.edit_text(_('👨‍💻 Админка'), reply_markup=markups.admin_panel())
