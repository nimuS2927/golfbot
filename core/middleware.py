from typing import Any, Dict, Callable, Awaitable
from aiogram import Bot, BaseMiddleware
from aiogram.types import Message, TelegramObject
from aiohttp import ClientSession


class SessionMiddleware(BaseMiddleware):
    def __init__(
            self,
            session: ClientSession,
    ) -> None:
        self.session = session

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
    ) -> Any:
        data['session'] = self.session
        return await handler(event, data)
