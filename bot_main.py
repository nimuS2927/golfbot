import asyncio
import logging
import logging.config
import time

import aiohttp
from aiohttp import ClientSession
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram_dialog import setup_dialogs

from core.config import c_bot
from core.config_logging import LOGGING
from core.dialogs.services.common import CommonService
from core.dialogs.windows import all_dialogs
from core.main.commands import set_commands
from core.middleware import SessionMiddleware
from core.main.handlers import client_router


logger = logging.getLogger(__name__)
logging.config.dictConfig(LOGGING)


async def on_start_bot(bot: Bot):
    await set_commands(bot)
    await bot.send_message(chat_id=1817810653, text=f'Bot started')


async def on_stop_bot(bot: Bot):
    await bot.send_message(chat_id=1817810653, text=f'Bot stopped')


async def main():
    logger.info('Start bot')
    storage = MemoryStorage()
    bot = Bot(token=c_bot.token)
    dp = Dispatcher(storage=storage)
    session = ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False))
    dp.update.middleware.register(SessionMiddleware(session=session))
    dialogs = all_dialogs()
    dp.include_router(client_router)
    # dp.include_router(registration_router)
    for dialog in dialogs:
        dp.include_router(dialog)

    setup_dialogs(dp)
    # Создание экземпляров бота и диспетчера
    # Настройка базового логирования

    # Регистрация действий на начало и окончание работы бота
    time.sleep(3)
    service = CommonService()
    await service.presets(session=session)
    dp.startup.register(on_start_bot)
    dp.shutdown.register(on_stop_bot)
    try:
        await dp.start_polling(bot)
    finally:
        await session.close()


if __name__ == '__main__':
    asyncio.run(main())
