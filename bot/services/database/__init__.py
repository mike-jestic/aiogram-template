from tortoise import Tortoise

from ...bot import bot

TORTOISE_ORM = {
    "connections": {"default": bot.config.database_uri},
    "apps": {
        "models": {
            "models": ["bot.services.database.models", "aerich.models"],
            "default_connection": "default",
        },
    },
}


class DatabaseService:
    async def setup(self):
        await Tortoise.init(TORTOISE_ORM)
        await Tortoise.generate_schemas()

    async def dispose(self):
        await Tortoise.close_connections()
