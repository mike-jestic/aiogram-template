from aiogram.fsm.state import State, StatesGroup


class MailingState(StatesGroup):
    waiting_msg = State()
    waiting_choose = State()
    waiting_recipient = State()

class GetUserState(StatesGroup):
    waiting_user_id = State()

class CreateMetricState(StatesGroup):
    waiting_name = State()
    waiting_desc = State()

class DelMetricState(StatesGroup):
    waiting_name = State()
