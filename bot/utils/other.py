from aiogram.types import BotCommand
from aiogram import Bot

async def set_commands(bot: Bot, dct_commands):
    for language_code, commands in dct_commands.items():
        command_list = []
        for command, description in commands.items():
            command_list.append(BotCommand(command=command, description=description))
        
        await bot.set_my_commands(command_list, language_code=language_code)
