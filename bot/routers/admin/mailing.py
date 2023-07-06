import asyncio

from aiogram.filters import Text
from aiogram import F, Bot, types
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as _
from aiogram.exceptions import TelegramBadRequest

from . import router
from ... import markups
from ...state import MailingState
from ...services.database.models import BotUser


@router.callback_query(Text('admin_mailing'))
async def admin_callback(call: types.CallbackQuery, state: FSMContext):
    await state.set_state(MailingState.waiting_msg)

    text = _('📨Пришлите сообщение для рассылки (Фото, текст, видео, голосовое сообщение):\n\n'
            '<em>Будьте осторожны, текст нужно вводить строго одним сообщением!</em>')
    
    return await call.message.edit_text(text, reply_markup=markups.back_admin())


@router.message(MailingState.waiting_msg, flags={"del_murkap": True})
async def get_message_to_send(message: types.Message, state: FSMContext):
    await state.update_data(message=message)
    await state.set_state(MailingState.waiting_choose)
    await message.answer(_('<b>Отправить?</b>'), reply_markup=markups.sending_keyboard())


@router.callback_query(MailingState.waiting_choose)
async def send_mailing_accept(call: types.CallbackQuery, state: FSMContext, bot: Bot):
    if call.data == 'one':
        await state.set_state(MailingState.waiting_recipient)
        return call.message.answer(_('<b>Пришлите id или username пользователя</b>'))
    
    elif call.data == 'cancel':
        await state.clear()
        return call.message.edit_text(
            _('✉ <b>Рассылка успешно отменена ❌</b>'),
            reply_markup=markups.admin_panel()
        )

    send, not_send = 0, 0
    users = await BotUser.exclude(active=False).all()

    await call.message.edit_text(_('📨 <b>Рассылка запущена </b>'), reply_markup=markups.admin_panel())

    data = await state.get_data()
    await state.clear()

    for user in users:
        try:
            await bot.copy_message(user.id, call.from_user.id, data['message'].message_id)
            send += 1
        except TelegramBadRequest:
            not_send += 1
            user.active = False
            await user.save()
        finally:
            await asyncio.sleep(0.2)
    
    text = _('✉ <b>Рассылка окончена!</b>\n\nДоставлено <code>{}</code> пользователям ✅\n'
            'Заблокировали бота <code>{}</code> пользователей ❌').format(send, not_send)

    await call.message.answer(text)


@router.message(F.text, MailingState.waiting_recipient)
async def send_mailing_admin(message: types.Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    await state.clear()

    user_data = message.text.replace('@', '')
    
    user = await BotUser.get_user(user_data)

    if not user:
        return message.answer(
            _('Пользователь не найден'),
            reply_markup=markups.admin_panel()
        )
    
    try:
        await bot.copy_message(user.id, message.from_user.id, data['message'].message_id)
        text = _('Успешно отправлено ✅')
    except TelegramBadRequest:
        text = _('Не отправлено. Пользователь заблокировал бота 🙁')

        user.active = False
        await user.save()   

    await bot.send_message(
        message.from_user.id, text,
        reply_markup=markups.admin_panel()
    )

