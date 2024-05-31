from typing import Dict, Union

from aiohttp import ClientSession
from pydantic import ValidationError
from requests import HTTPError

from core.dialogs.schemas.admins import AdminSchemas, CreateAdmin, SuperUser, GetAdmin
from core.dialogs.services.base import BaseService


class AdminService(BaseService):
    _model = AdminSchemas

    async def get_admin_by_login(
            self,
            session: ClientSession,
            admin_form: GetAdmin,
    ) -> bool:
        """ По логину и паролю"""
        async with session.post(
                self.api_urls.post_admin_by_login(),
                json=admin_form.model_dump()
        ) as response_post:
            if response_post.status == 200:
                return True
            elif response_post.status == 401:
                return False
            else:
                raise HTTPError('Server error')

    async def get_admin_authorization(
            self,
            session: ClientSession,
            login: str,
    ) -> bool:
        """ По логину для суперпользователя"""
        superuser: SuperUser = SuperUser(
            login=self.set_service.login_superuser,
            password=self.set_service.password_superuser,
        )
        async with session.post(
                self.api_urls.post_admin_authorization_for_superuser(login=login),
                json=superuser.model_dump()
        ) as response_post:
            if response_post.status == 200:
                return True
            elif response_post.status == 401:
                return False
            else:
                raise HTTPError('Server error')

    async def post_create_admin(
            self,
            session: ClientSession,
            admin_form: CreateAdmin,
    ) -> bool:
        """ По логину для суперпользователя"""
        superuser: SuperUser = SuperUser(
            login=self.set_service.login_superuser,
            password=self.set_service.password_superuser,
        )

        async with session.post(
                self.api_urls.post_admin(),
                json={'superuser_in': superuser, 'admin_in': admin_form}
        ) as response_post:
            if response_post.status == 201:
                return True
            elif response_post.status == 401:
                return False
            else:
                raise HTTPError('Server error')

    async def delete_admin_by_login(
            self,
            session: ClientSession,
            login: str,
    ) -> bool:
        """ По логину для суперпользователя"""
        superuser: SuperUser = SuperUser(
            login=self.set_service.login_superuser,
            password=self.set_service.password_superuser,
        )
        async with session.delete(
                self.api_urls.delete_admin_by_login(login=login),
                json=superuser
        ) as response_post:
            if response_post.status == 204:
                return True
            elif response_post.status == 401:
                return False
            else:
                raise HTTPError('Server error')
