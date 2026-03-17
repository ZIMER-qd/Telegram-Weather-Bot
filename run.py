import asyncio
import logging
from aiogram import Dispatcher, types
from aiohttp import ClientSession

from app.handlers import command_router, fsmessage_router, fsmnotify_router
from app.callbacks import callback_router, pagination_router

from app.database.models import async_main

import app.services.sessions as session_module
from app.services.bot_instance import bot
from app.services.scheduler import start_scheduler


logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

dp = Dispatcher()


async def set_commands():
    commands = [
        types.BotCommand(command='start', description='Запуск'),
        types.BotCommand(command='weather', description='Узнать погоду'),
        types.BotCommand(command='help', description='Помощь')
    ]
    
    await bot.set_my_commands(commands)


async def main():
    try:
        await async_main()
    except Exception as e:
        logging.error(f"Database initialization failed: {e}")
        return
    
    try:
        start_scheduler(bot)
    except Exception as e:
        logging.error(f"Scheduler initialization failed: {e}")
        return
    
    session_module.session = ClientSession()
    dp.include_routers(command_router,
                       pagination_router,
                       callback_router,
                       fsmnotify_router,
                       fsmessage_router)

    try:
        await set_commands()
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    finally:
        if session_module.session:
            await session_module.session.close()
            logging.info("HTTP session closed.")

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Bot stopped!")