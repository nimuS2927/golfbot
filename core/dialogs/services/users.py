from typing import Dict, Union

from aiohttp import ClientSession
from pydantic import ValidationError
from requests import HTTPError

from core.dialogs.schemas.users import User, CreateUser, UpdateUser, UpdateUserPartial
from core.dialogs.services.base import BaseService


class UserService(BaseService):
    _model = User

    async def get_user(
            self,
            session: ClientSession,
            user_id: int
    ) -> User:
        headers = await self.create_headers(session=session)
        async with session.get(
            self.api_urls.get_user_by_id(user_id),
            headers=headers,
        ) as response:
            if response.status == 200:
                obj_dict = await response.json()
                return self._model.model_validate(obj_dict)
            if response.status == 422:
                raise ValidationError('Invalid user id')
            raise HTTPError('Server error')

    async def update_user(
            self,
            session: ClientSession,
            user_id: int,
            data: UpdateUser
    ) -> User:
        headers = await self.create_headers(session=session)
        async with session.get(
            self.api_urls.put_user_by_id(user_id),
            headers=headers,
            json=data,
        ) as response:
            if response.status == 200:
                obj_dict = await response.json()
                return self._model.model_validate(obj_dict)
            if response.status == 422:
                raise ValidationError('Invalid user fields')
            raise HTTPError('Server error')

    async def partial_update_user(
            self,
            session: ClientSession,
            user_id: int,
            data: UpdateUserPartial
    ) -> User:
        headers = await self.create_headers(session=session)
        async with session.get(
            self.api_urls.patch_user_by_id(user_id),
            headers=headers,
            json=data,
        ) as response:
            if response.status == 200:
                obj_dict = await response.json()
                return self._model.model_validate(obj_dict)
            if response.status == 422:
                raise ValidationError('Invalid user fields')
            raise HTTPError('Server error')

    async def delete_user(
            self,
            session: ClientSession,
            user_id: int
    ) -> str:
        headers = await self.create_headers(session=session)
        async with session.delete(
            self.api_urls.delete_user_by_id(user_id),
            headers=headers,
        ) as response:
            if response.status == 204:
                return await response.json()
            if response.status == 422:
                raise ValidationError('Invalid user id')
            raise HTTPError('Server error')

    async def get_user_by_tg_id(
            self,
            session: ClientSession,
            tg_id: int
    ) -> User:
        headers = await self.create_headers(session=session)
        async with session.get(
            self.api_urls.get_user_by_tg_id(tg_id),
            headers=headers,
        ) as response:
            if response.status == 200:
                obj_dict = await response.json()
                return self._model.model_validate(obj_dict)
            if response.status == 422:
                raise ValidationError('Invalid user tg id')
            raise HTTPError('Server error')

    async def create_user(
            self,
            session: ClientSession,
            data: CreateUser
    ) -> User:
        headers = await self.create_headers(session=session)
        print(data)
        async with session.post(
            self.api_urls.post_user(),
            headers=headers,
            json=data,
        ) as response:
            if response.status == 201:
                obj_dict = await response.json()
                return self._model.model_validate(obj_dict)
            if response.status == 422:
                raise ValidationError('Invalid user fields')
            raise HTTPError('Server error')
