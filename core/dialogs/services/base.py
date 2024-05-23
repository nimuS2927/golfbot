from typing import Dict

import jwt
from aiohttp import ClientSession

from core.dialogs.api_urls import ApiURL
from core.dialogs.services.common import CommonService


class BaseService:
    def __init__(self):
        self.set_service = CommonService()
        self.api_urls = ApiURL()

    async def create_headers(
            self,
            session: ClientSession,
    ) -> Dict[str, str]:
        token = self.set_service.access_token
        try:
            await self.set_service.check_token(token)
        except jwt.ExpiredSignatureError or jwt.InvalidTokenError:
            await self.set_service.get_access_token(session=session)
            token = self.set_service.access_token
        return {'Authorization': token}
