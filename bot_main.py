import asyncio
import logging

import aiohttp
from aiohttp import ClientSession
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram_dialog import setup_dialogs

from core.config import c_bot
# from core.dialogs.main_menu.services.common import CommonService, SessionMiddleware
# from core.utils.commands import set_commands
from core.main.handlers import client_router, registration_router
# from core.dialogs.main_menu import states
# from core.dialogs.main_menu.windows import AllWindows, all_dialogs
from core.middleware import SessionMiddleware


async def on_start_bot(bot: Bot):
    await bot.send_message(chat_id=1817810653, text=f'Bot started')


async def on_stop_bot(bot: Bot):
    await bot.send_message(chat_id=1817810653, text=f'Bot stopped')


async def main():

    storage = MemoryStorage()
    bot = Bot(token=c_bot.token)
    dp = Dispatcher(storage=storage)
    session = ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False))
    dp.update.middleware.register(SessionMiddleware(session=session))
    # dialogs = all_dialogs()
    dp.include_router(client_router)
    dp.include_router(registration_router)
    # for dialog in dialogs:
    #     dp.include_router(dialog)

    setup_dialogs(dp)
    # Создание экземпляров бота и диспетчера
    # Настройка базового логирования
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(name)s -'
                               ' %(message)s')

    # Регистрация действий на начало и окончание работы бота
    # service = CommonService()
    # await service.presets(session=session)
    dp.startup.register(on_start_bot)
    dp.shutdown.register(on_stop_bot)
    try:
        await dp.start_polling(bot)
    finally:
        await session.close()


if __name__ == '__main__':
    asyncio.run(main())
