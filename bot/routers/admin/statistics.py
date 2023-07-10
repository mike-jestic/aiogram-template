from aiogram import Bot, types
from aiogram.filters import Text
from aiogram.utils.i18n import gettext as _
from aiogram.utils.deep_linking import create_start_link

from . import router
from ... import markups
from ...services.database.models import Metric, BotUser


@router.callback_query(Text('admin_statistics'))
async def get_statistics_callback(call: types.CallbackQuery, bot: Bot):
    await send_statistics(bot, call.message)


async def send_statistics(bot: Bot, message: types.Message):
    metrics = await Metric.get_metrics()

    count_users = await BotUser.all().count()
    active_users = await BotUser.filter(active=True).count()
    blocked_users = await BotUser.filter(active=False).count()
    ban_users = await BotUser.filter(is_banned=True).count()

    msg = _(
        '📈 Пользователи\nВсего: {}\nАктивные: {}\nЗабанено: {}\nЗаблокировали бота: {}\n\n'
    ).format(count_users, active_users, blocked_users, ban_users)

    if metrics:
        msg += _('📊 Метрика\n')

    for m in metrics:
        link = await create_start_link(bot, m['code'])
        msg += f"<code>{link}</code>\n👥 {m['count']}"
        msg += f" • {m['desc']} \n\n"

    top_referrers = await BotUser.get_top_referrers()
    msg += _('🏆 Топ рефереров\n')
    for n, data in enumerate(top_referrers):
        msg += f"{n+1}. {data.user.url} - {data.referral_count}\n"

    if message.from_user.is_bot:
        await message.edit_text(msg, reply_markup=markups.add_event())
    else:
        await message.answer(msg, reply_markup=markups.add_event())
