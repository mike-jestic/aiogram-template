import re

from aiogram import F, Bot, types
from aiogram.utils.i18n import gettext as _
from aiogram.fsm.context import FSMContext

from . import router
from ... import markups
from .statistics import send_statistics
from ...services.database.models import Metric
from ...state import CreateMetricState, DelMetricState


@router.callback_query(F.data == 'del_metric')
async def admin_callback(call: types.CallbackQuery, state: FSMContext):
    await state.set_state(DelMetricState.waiting_name)

    await call.message.answer(_('Введите код метрики или ссылку для удаления'))


@router.message(DelMetricState.waiting_name)
async def admin_callback(message: types.Message, state: FSMContext):

    text = message.text
    code = text if not '?start=' in text else text.split('?start=')[1]
    
    metric = await Metric.get_or_none(code=code)
    if not metric:
        await state.clear()
        return message.answer(_('Такой метрики не существует'))

    await message.answer(
        _('Вы действительно хотите удалить метрику'),
        reply_markup=markups.question_delete_entity(metric.id, 'metric'))

    await state.clear()

@router.callback_query(F.data  == 'add_metric')
async def admin_callback(call: types.CallbackQuery, state: FSMContext):
    await state.set_state(CreateMetricState.waiting_name)

    await call.message.answer(_('Введите код метрики'))

@router.message(CreateMetricState.waiting_name)
async def admin_callback(message: types.Message, state: FSMContext):

    if re.search(r"[^_A-z0-9-]", message.text) or message.text.isdecimal():
        await state.clear()
        return message.answer(_('Код должен содержать A-Z, a-z, 0-9 и хотя бы одну букву'))
    
    metric = await Metric.get_or_none(code=message.text)
    if metric:
        await state.clear()
        return message.answer(_('Такой код уже существует'))

    await state.update_data(code=message.text)
    await state.set_state(CreateMetricState.waiting_desc)
    
    await message.answer(_('Введите описание'))

@router.message(CreateMetricState.waiting_desc)
async def admin_callback(message: types.Message, state: FSMContext, bot: Bot):
    code = (await state.get_data())['code']
    await state.clear()

    await Metric.create(
        code=code,
        description=message.text
    )

    await message.answer(_('Метрика успешно созданна'))

    await send_statistics(bot, message)