import logging
from typing import Dict

import jwt
from aiohttp import ClientSession

from core.dialogs.api_urls import ApiURL
from core.dialogs.services.common import CommonService


logger = logging.getLogger(__name__)


class BaseService:
    def __init__(self):
        self.set_service = CommonService()
        self.api_urls = ApiURL()

    async def create_headers(
            self,
            session: ClientSession,
    ) -> Dict[str, str]:
        logger.debug("start Creating headers")
        token = self.set_service.access_token
        try:
            await self.set_service.check_token(token)
        except jwt.ExpiredSignatureError or jwt.InvalidTokenError:
            logger.debug("fail checking accesses token")
            await self.set_service.get_access_token(session=session)
            token = self.set_service.access_token
        logger.debug("Stop Creating headers")
        return {'Authorization': token}
