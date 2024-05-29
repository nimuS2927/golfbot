from typing import Dict, Union, List, Any

from aiohttp import ClientSession
from pydantic import ValidationError
from requests import HTTPError

from core.dialogs.schemas.scores import Score, CreateScore, UpdateScore, UpdateScorePartial
from core.dialogs.services.base import BaseService


class ScoreService(BaseService):
    _model = Score

    async def get_score_by_id(
            self,
            session: ClientSession,
            score_id: int
    ) -> Score:
        headers = await self.create_headers(session=session)
        async with session.get(
            self.api_urls.get_score_by_id(score_id),
            headers=headers,
        ) as response:
            if response.status == 200:
                obj_dict = await response.json()
                return self._model.model_validate(obj_dict)
            if response.status == 422:
                raise ValidationError('Invalid score id')
            raise HTTPError('Server error')

    async def get_scores_all(
            self,
            session: ClientSession,
    ) -> List[Score]:
        headers = await self.create_headers(session=session)
        async with session.get(
            self.api_urls.get_scores(),
            headers=headers,
        ) as response:
            if response.status == 200:
                objs_dict = await response.json()
                return [self._model.model_validate(dict_data) for dict_data in objs_dict]
            if response.status == 422:
                raise ValidationError('Invalid request')
            raise HTTPError('Server error')

    async def get_score_by_id_tournament(
            self,
            id_tournament: int,
            session: ClientSession,
    ) -> List[Score]:
        headers = await self.create_headers(session=session)
        async with session.get(
            self.api_urls.get_score_by_id_tournament(id_tournament=id_tournament),
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

    async def get_score_by_id_tournament_and_id_hole(
            self,
            id_tournament: int,
            id_hole: int,
            session: ClientSession,
    ) -> List[Score]:
        headers = await self.create_headers(session=session)
        async with session.get(
            self.api_urls.get_score_by_id_tournament_and_id_hole(id_tournament=id_tournament, id_hole=id_hole),
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

    async def get_scores_by_id_tournament_and_id_user(
            self,
            id_tournament: int,
            id_user: int,
            session: ClientSession,
    ) -> List[Score]:
        headers = await self.create_headers(session=session)
        async with session.get(
                self.api_urls.get_scores_by_id_tournament_and_id_user(id_tournament=id_tournament, id_user=id_user),
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

    async def update_score(
            self,
            session: ClientSession,
            score_id: int,
            data: UpdateScore
    ) -> Score:
        headers = await self.create_headers(session=session)
        async with session.get(
            self.api_urls.put_score_by_id(score_id),
            headers=headers,
            json=data,
        ) as response:
            if response.status == 200:
                obj_dict = await response.json()
                return self._model.model_validate(obj_dict)
            if response.status == 422:
                raise ValidationError('Invalid score fields')
            raise HTTPError('Server error')

    async def partial_update_score(
            self,
            session: ClientSession,
            score_id: int,
            data: UpdateScorePartial
    ) -> Score:
        headers = await self.create_headers(session=session)
        async with session.patch(
            self.api_urls.patch_score_by_id(score_id),
            headers=headers,
            json=data,
        ) as response:
            if response.status == 200:
                obj_dict = await response.json()
                return self._model.model_validate(obj_dict)
            if response.status == 422:
                raise ValidationError('Invalid score fields')
            raise HTTPError('Server error')

    async def delete_score(
            self,
            session: ClientSession,
            score_id: int
    ) -> str:
        headers = await self.create_headers(session=session)
        async with session.delete(
            self.api_urls.delete_score_by_id(score_id),
            headers=headers,
        ) as response:
            if response.status == 204:
                return await response.json()
            if response.status == 422:
                raise ValidationError('Invalid score id')
            raise HTTPError('Server error')

    async def create_score(
            self,
            session: ClientSession,
            data: CreateScore
    ) -> Score:
        headers = await self.create_headers(session=session)
        async with session.post(
            self.api_urls.post_score(),
            headers=headers,
            json=data,
        ) as response:
            if response.status == 201:
                obj_dict = await response.json()
                return self._model.model_validate(obj_dict)
            if response.status == 422:
                raise ValidationError('Invalid score fields')
            raise HTTPError('Server error')

    async def create_scores(
            self,
            session: ClientSession,
            data: List[CreateScore]
    ) -> List[Score]:
        headers = await self.create_headers(session=session)
        async with session.post(
            self.api_urls.post_scores(),
            headers=headers,
            json=data,
        ) as response:
            if response.status == 201:
                objs_dict = await response.json()
                return [self._model.model_validate(dict_data) for dict_data in objs_dict]
            if response.status == 422:
                raise ValidationError('Invalid score fields')
            raise HTTPError('Server error')




