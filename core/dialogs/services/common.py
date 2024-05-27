import asyncio
import logging

from aiohttp import ClientSession
import jwt

from requests import HTTPError

from core.config import c_project
from core.dialogs.api_urls import ApiURL


logger = logging.getLogger(__name__)


class CommonService:
    _instance = None
    _access_token = None
    _refresh_token = None
    _algorithm = None
    _public_key = None
    prefix_exception = 'ex'

    def __init__(self):
        self._login_superuser = c_project.api.login_superuser
        self._password_superuser = c_project.api.password_superuser
        self.api_urls = ApiURL()

    def __new__(cls):
        if not cls._instance:
            instance = super(CommonService, cls).__new__(cls)
            cls._instance = instance
        return cls._instance

    # region Functions to getting, to setting and to deleting Base Service parameters
    # region Functions GSD access token
    @property
    def access_token(self):
        return self._access_token

    @access_token.setter
    def access_token(self, value):
        self._access_token = value

    @access_token.deleter
    def access_token(self):
        self._access_token = None

    # endregion
    # region Functions GSD refresh token
    @property
    def refresh_token(self):
        return self._refresh_token

    @refresh_token.setter
    def refresh_token(self, value):
        self._refresh_token = value

    @refresh_token.deleter
    def refresh_token(self):
        self._refresh_token = None

    # endregion
    # region Functions GSD algorithm
    @property
    def algorithm(self):
        return self._algorithm

    @algorithm.setter
    def algorithm(self, value):
        self._algorithm = value

    @algorithm.deleter
    def algorithm(self):
        self._algorithm = None

    # endregion
    # region Functions GSD public key
    @property
    def public_key(self):
        return self._public_key

    @public_key.setter
    def public_key(self, value):
        self._public_key = value

    @public_key.deleter
    def public_key(self):
        self._public_key = None

    # endregion
    # region Functions GET login and password superuser
    @property
    def login_superuser(self):
        return self._login_superuser

    @property
    def password_superuser(self):
        return self._password_superuser

    # endregion
    # endregion

    async def presets(
            self,
            session: ClientSession,
            login: str = c_project.bot.admin_id,
            password: str = c_project.bot.admin_password,
    ):
        lock = asyncio.Lock()
        async with lock:
            await self.check_admin(
                    login=login,
                    password=password,
                    session=session,
                )
        async with lock:
            await self.get_both_tokens(
                login=login,
                password=password,
                session=session,
            )

    async def check_admin(
            self,
            session: ClientSession,
            login: str = c_project.bot.admin_id,
            password: str = c_project.bot.admin_password,
    ) -> bool:
        data = {
            "admin_in": {
                "login": login,
                "password": password
            },
            "superuser_in": {
                "login": str(self.login_superuser),
                "password": str(self.password_superuser)
            }
        }
        async with session.get(
                self.api_urls.get_admin_by_login(),
                params=data['admin_in']
        ) as response_get:
            if response_get.status == 200:
                return True
            elif response_get.status == 401:
                async with session.post(
                        self.api_urls.post_admin(),
                        data=data
                ) as response_post:
                    if response_post.status == 201:
                        return True
                    elif response_post.status == 401:
                        raise ValueError('Invalid superuser parameters')
                    else:
                        raise HTTPError('Server error in')
            else:
                raise HTTPError('Server error out')

    async def check_token(
            self,
            token: str | bytes,
    ) -> str | dict:
        logger.debug("start Checking token")
        decoded = jwt.decode(
            token.split()[1],
            self.public_key,
            algorithms=[self.algorithm],
        )
        logger.debug("successful Checking token")
        return token

    async def get_access_token(
            self,
            session: ClientSession,
            login: str = c_project.bot.admin_id,
            password: str = c_project.bot.admin_password,
    ) -> None:
        logger.debug("start Getting new access token use refresh token")

        try:
            lock = asyncio.Lock()
            async with lock:
                logger.debug("start checking refresh token")
                check_token = self.refresh_token
                result = await self.check_token(token=check_token)
            async with lock:
                headers = {'Authorization': self.refresh_token}
                logger.debug("post request for getting access token")
                async with session.post(
                        self.api_urls.post_refresh_access_token(),
                        headers=headers,
                ) as response_post:
                    if response_post.status == 201:
                        logger.info("successful getting access token")
                        resp_data = await response_post.json()
                        self.access_token = resp_data['access_token']
                    else:
                        logger.info("fail getting access token")
                        raise HTTPError('Server error')
        except jwt.ExpiredSignatureError or jwt.InvalidTokenError:
            logger.debug("fail checking refresh token")
            await self.get_both_tokens(
                login=login,
                password=password,
                session=session,
            )

    async def get_both_tokens(
            self,
            session: ClientSession,
            login: str = c_project.bot.admin_id,
            password: str = c_project.bot.admin_password,
    ) -> None:
        data = {
            "login": login,
            "password": password
        }
        logger.debug("post request for getting both tokens")
        async with session.post(
                self.api_urls.post_tokens(),
                json=data
        ) as response_post:
            if response_post.status == 201:
                logger.info("successful getting both tokens")
                resp_data = await response_post.json()
                self.access_token = resp_data["access_token"]
                self.refresh_token = resp_data["refresh_token"]
                self.public_key = resp_data["public_key"]
                self.algorithm = resp_data["algorithm"]
            elif response_post.status == 401:
                logger.info("Invalid login or password")
                raise ValueError('Invalid login or password')
            else:
                logger.info("fail getting access token")
                raise HTTPError('Server error')
