from ..utils.dispatcher import Dispatcher
from .database import DatabaseService
from .schedule import ScheduleService, jobs


async def setup(dispatcher: Dispatcher):
    schedule_service = ScheduleService()
    database_service = DatabaseService()

    dispatcher.services.register(database_service)
    dispatcher.services.register(schedule_service)

    await dispatcher.services.setup_all()


async def dispose(dispatcher: Dispatcher):
    await dispatcher.services.dispose_all()
