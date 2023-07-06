import logging
from . import middleware, routers, services
from .bot import bot, dispatcher
from .utils.paths import root_path, routers_path
from .utils.other import set_commands

@dispatcher.startup()
async def on_startup():

    dct_commands = {
        'ru': {
            'start': '🔄 Перезапустить бота',
        },
        
        'en': {
            'start': '🔄 Restart bot'
        }
    }

    await set_commands(bot, dct_commands)

    await services.setup(dispatcher)

    me = await bot.get_me()
    print(f'Бот запущен! {me.username}')


@dispatcher.shutdown()
async def on_shutdown():
    await services.dispose(dispatcher)

def import_routers():
    for router_path in routers_path.glob("*"):
        if router_path.stem.startswith("__") and router_path.stem.endswith("__"):
            continue

        if router_path.is_file():
            __import__(f"bot.routers.{router_path.stem}")
            continue

        sorted_handler_file_paths = sorted(
            router_path.glob("*.*"), key=lambda p: p.stem
        )

        for handler_file_path in sorted_handler_file_paths:
            if not handler_file_path.is_file():
                continue

            __import__(f"bot.routers.{router_path.stem}.{handler_file_path.stem}")


def main():
    log_filename = str((root_path / "logs.log").resolve())

    logging.basicConfig(
        # filename=log_filename,
        level=logging.ERROR,
        format=r"%(asctime)s %(levelname)s %(funcName)s(%(lineno)d) %(message)s",
    )

    middleware.setup(dispatcher)
    import_routers()
    dispatcher.include_router(routers.root_handlers_router)

    used_update_types = dispatcher.resolve_used_update_types()
    dispatcher.run_polling(bot, allowed_updates=used_update_types)


if __name__ == '__main__':
    main()
