from aiogram.filters.callback_data import CallbackData
import typing

class ActionsWithUser(CallbackData, prefix="admin_user"):
    user_id: int
    action: str

class DeleteCallbackData(CallbackData, prefix="delete_entity"):
    id: int
    type_entity: str
    

    