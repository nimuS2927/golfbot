from typing import Dict, Union, List, Any

from aiohttp import ClientSession
from pydantic import ValidationError
from requests import HTTPError

from core.dialogs.schemas.totalscores import TotalScore, CreateTotalScore, UpdateTotalScore, UpdateTotalScorePartial
from core.dialogs.services.base import BaseService


class TotalScoreService(BaseService):
    _model = TotalScore

    async def get_totalscore_by_id(
            self,
            session: ClientSession,
            totalscore_id: int
    ) -> TotalScore:
        headers = await self.create_headers(session=session)
        async with session.get(
            self.api_urls.get_totalscore_by_id(totalscore_id),
            headers=headers,
        ) as response:
            if response.status == 200:
                obj_dict = await response.json()
                return self._model.model_validate(obj_dict)
            if response.status == 422:
                raise ValidationError('Invalid totalscore id')
            raise HTTPError('Server error')

    async def get_totalscores_all(
            self,
            session: ClientSession,
    ) -> List[TotalScore]:
        headers = await self.create_headers(session=session)
        async with session.get(
            self.api_urls.get_totalscores(),
            headers=headers,
        ) as response:
            if response.status == 200:
                objs_dict = await response.json()
                return [self._model.model_validate(dict_data) for dict_data in objs_dict]
            if response.status == 422:
                raise ValidationError('Invalid request')
            raise HTTPError('Server error')

    async def get_totalscore_by_id_tournament(
            self,
            id_tournament: int,
            session: ClientSession,
    ) -> List[TotalScore]:
        headers = await self.create_headers(session=session)
        async with session.get(
            self.api_urls.get_totalscore_by_id_tournament(id_tournament=id_tournament),
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

    async def get_totalscore_by_id_tournament_and_id_user(
            self,
            id_tournament: int,
            id_user: int,
            session: ClientSession,
    ) -> List[TotalScore]:
        headers = await self.create_headers(session=session)
        async with session.get(
                self.api_urls.get_totalscore_by_id_tournament_and_id_user(id_tournament=id_tournament, id_user=id_user),
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

    async def update_totalscore(
            self,
            session: ClientSession,
            totalscore_id: int,
            data: UpdateTotalScore
    ) -> TotalScore:
        headers = await self.create_headers(session=session)
        async with session.get(
            self.api_urls.put_totalscore_by_id(totalscore_id),
            headers=headers,
            json=data,
        ) as response:
            if response.status == 200:
                obj_dict = await response.json()
                return self._model.model_validate(obj_dict)
            if response.status == 422:
                raise ValidationError('Invalid totalscore fields')
            raise HTTPError('Server error')

    async def partial_update_totalscore(
            self,
            session: ClientSession,
            totalscore_id: int,
            data: UpdateTotalScorePartial
    ) -> TotalScore:
        headers = await self.create_headers(session=session)
        async with session.get(
            self.api_urls.patch_totalscore_by_id(totalscore_id),
            headers=headers,
            json=data,
        ) as response:
            if response.status == 200:
                obj_dict = await response.json()
                return self._model.model_validate(obj_dict)
            if response.status == 422:
                raise ValidationError('Invalid totalscore fields')
            raise HTTPError('Server error')

    async def delete_totalscore(
            self,
            session: ClientSession,
            totalscore_id: int
    ) -> str:
        headers = await self.create_headers(session=session)
        async with session.delete(
            self.api_urls.delete_totalscore_by_id(totalscore_id),
            headers=headers,
        ) as response:
            if response.status == 204:
                return await response.json()
            if response.status == 422:
                raise ValidationError('Invalid totalscore id')
            raise HTTPError('Server error')

    async def create_totalscore(
            self,
            session: ClientSession,
            data: CreateTotalScore
    ) -> TotalScore:
        headers = await self.create_headers(session=session)
        async with session.post(
            self.api_urls.post_totalscore(),
            headers=headers,
            json=data,
        ) as response:
            if response.status == 201:
                obj_dict = await response.json()
                return self._model.model_validate(obj_dict)
            if response.status == 422:
                raise ValidationError('Invalid totalscore fields')
            raise HTTPError('Server error')




