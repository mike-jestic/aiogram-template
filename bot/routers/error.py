import logging
import traceback

from ..utils.router import Router
from . import root_handlers_router as router
from aiogram.types.error_event import ErrorEvent

from aiogram.filters import ExceptionTypeFilter
from aiogram.types import CallbackQuery
from aiogram.exceptions import TelegramBadRequest


@router.errors()
async def errors_handler(error: Exception):
    logging.error(error, exc_info=True)
    return True    


# @router.errors(F.update.callback_query.as_("query"))
# async def callback_query_error_handler(event: ErrorEvent, query: CallbackQuery) -> None:
"""
  Error Handler для случаев с Inline Callback Query.
  """

#   pass

# @router.errors(ExceptionTypeFilter(TelegramBadRequest))
# async def get_errors(ex: ErrorEvent, **data):
#     print(ex)
