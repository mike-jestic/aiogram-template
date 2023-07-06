from aiogram.fsm.storage.memory import MemoryStorage

from .models.config.bot_config import BotConfig
from .utils.bot import Bot
from .utils.dispatcher import Dispatcher


bot = Bot(BotConfig.load_first(), parse_mode="html")
dispatcher = Dispatcher(storage=MemoryStorage())

