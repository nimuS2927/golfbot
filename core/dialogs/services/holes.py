from typing import Dict, Union, List, Any

from aiohttp import ClientSession
from pydantic import ValidationError
from requests import HTTPError

from core.dialogs.schemas.holes import Hole, CreateHole, UpdateHole, UpdateHolePartial
from core.dialogs.services.base import BaseService


class HoleService(BaseService):
    _model = Hole

    async def get_hole_by_id(
            self,
            session: ClientSession,
            hole_id: int
    ) -> Hole:
        headers = await self.create_headers(session=session)
        async with session.get(
            self.api_urls.get_hole_by_id(hole_id),
            headers=headers,
        ) as response:
            if response.status == 200:
                obj_dict = await response.json()
                return self._model.model_validate(obj_dict)
            if response.status == 422:
                raise ValidationError('Invalid hole id')
            raise HTTPError('Server error')

    async def get_holes_all(
            self,
            session: ClientSession,
    ) -> List[Hole]:
        headers = await self.create_headers(session=session)
        async with session.get(
            self.api_urls.get_holes(),
            headers=headers,
        ) as response:
            if response.status == 200:
                objs_dict = await response.json()
                return [self._model.model_validate(dict_data) for dict_data in objs_dict]
            if response.status == 422:
                raise ValidationError('Invalid request')
            raise HTTPError('Server error')

    async def get_holes_by_course_id(
            self,
            course_id: int,
            session: ClientSession,
    ) -> List[Hole]:
        headers = await self.create_headers(session=session)
        async with session.get(
            self.api_urls.get_holes_by_course_id(id_course=course_id),
            headers=headers,
        ) as response:
            if response.status == 200:
                objs_dict = await response.json()
                return [self._model.model_validate(dict_data) for dict_data in objs_dict]
            if response.status == 404:
                return []
            if response.status == 422:
                raise ValidationError('Invalid request')
            raise HTTPError('Server error')

    async def update_hole(
            self,
            session: ClientSession,
            hole_id: int,
            data: UpdateHole
    ) -> Hole:
        headers = await self.create_headers(session=session)
        async with session.put(
            self.api_urls.put_hole_by_id(hole_id),
            headers=headers,
            json=data,
        ) as response:
            if response.status == 200:
                obj_dict = await response.json()
                return self._model.model_validate(obj_dict)
            if response.status == 422:
                raise ValidationError('Invalid hole fields')
            raise HTTPError('Server error')

    async def partial_update_hole(
            self,
            session: ClientSession,
            hole_id: int,
            data: UpdateHolePartial
    ) -> Hole:
        headers = await self.create_headers(session=session)
        async with session.patch(
            self.api_urls.patch_hole_by_id(hole_id),
            headers=headers,
            json=data,
        ) as response:
            if response.status == 200:
                obj_dict = await response.json()
                return self._model.model_validate(obj_dict)
            if response.status == 422:
                raise ValidationError('Invalid hole fields')
            raise HTTPError('Server error')

    async def delete_hole(
            self,
            session: ClientSession,
            hole_id: int
    ) -> str:
        headers = await self.create_headers(session=session)
        async with session.delete(
            self.api_urls.delete_hole_by_id(hole_id),
            headers=headers,
        ) as response:
            if response.status == 204:
                return await response.json()
            if response.status == 422:
                raise ValidationError('Invalid hole id')
            raise HTTPError('Server error')

    async def get_hole_by_number(
            self,
            session: ClientSession,
            number: int
    ) -> Hole:
        headers = await self.create_headers(session=session)
        async with session.get(
            self.api_urls.get_hole_by_number(number),
            headers=headers,
        ) as response:
            if response.status == 200:
                obj_dict = await response.json()
                return self._model.model_validate(obj_dict)
            if response.status == 422:
                raise ValidationError('Invalid hole tg id')
            raise HTTPError('Server error')

    async def create_hole(
            self,
            session: ClientSession,
            data: CreateHole
    ) -> Hole:
        headers = await self.create_headers(session=session)
        async with session.post(
            self.api_urls.post_hole(),
            headers=headers,
            json=data,
        ) as response:
            if response.status == 201:
                obj_dict = await response.json()
                return self._model.model_validate(obj_dict)
            if response.status == 422:
                raise ValidationError('Invalid hole fields')
            raise HTTPError('Server error')




