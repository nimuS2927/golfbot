from typing import Dict, Union, List, Any

from aiohttp import ClientSession
from pydantic import ValidationError
from requests import HTTPError

from core.dialogs.schemas.tournaments import Tournament, CreateTournament, UpdateTournament, UpdateTournamentPartial
from core.dialogs.services.base import BaseService


class TournamentService(BaseService):
    _model = Tournament

    async def get_tournament_by_id(
            self,
            session: ClientSession,
            tournament_id: int
    ) -> Tournament:
        headers = await self.create_headers(session=session)
        async with session.get(
            self.api_urls.get_tournament_by_id(tournament_id),
            headers=headers,
        ) as response:
            if response.status == 200:
                obj_dict = await response.json()
                return self._model.model_validate(obj_dict)
            if response.status == 422:
                raise ValidationError('Invalid tournament id')
            raise HTTPError('Server error')

    async def get_tournament_nearest(
            self,
            session: ClientSession,
    ) -> List[Tournament]:
        headers = await self.create_headers(session=session)
        async with session.get(
            self.api_urls.get_tournament_nearest(),
            headers=headers,
        ) as response:
            if response.status == 200:
                objs_dict = await response.json()
                return [self._model.model_validate(dict_data) for dict_data in objs_dict]
            if response.status == 422:
                raise ValidationError('Invalid tournament id')
            raise HTTPError('Server error')

    async def get_tournament_nearest_without_users(
            self,
            session: ClientSession,
            user_tg_id: int,
    ) -> List[Tournament]:
        headers = await self.create_headers(session=session)
        async with session.post(
            self.api_urls.post_tournament_nearest(),
            headers=headers,
            json={"user_tg_id": user_tg_id},
        ) as response:
            if response.status == 200:
                objs_dict = await response.json()
                return [self._model.model_validate(dict_data) for dict_data in objs_dict]
            if response.status == 404:
                return []
            if response.status == 422:
                raise ValidationError('Invalid tournament id')
            raise HTTPError('Server error')

    async def get_tournaments_all(
            self,
            session: ClientSession,
    ) -> List[Tournament]:
        headers = await self.create_headers(session=session)
        async with session.get(
            self.api_urls.get_tournaments(),
            headers=headers,
        ) as response:
            if response.status == 200:
                objs_dict = await response.json()
                return [self._model.model_validate(dict_data) for dict_data in objs_dict]
            if response.status == 422:
                raise ValidationError('Invalid request')
            raise HTTPError('Server error')

    async def update_tournament(
            self,
            session: ClientSession,
            tournament_id: int,
            data: UpdateTournament
    ) -> Tournament:
        headers = await self.create_headers(session=session)
        async with session.get(
            self.api_urls.put_tournament_by_id(tournament_id),
            headers=headers,
            json=data,
        ) as response:
            if response.status == 200:
                obj_dict = await response.json()
                return self._model.model_validate(obj_dict)
            if response.status == 422:
                raise ValidationError('Invalid tournament fields')
            raise HTTPError('Server error')

    async def partial_update_tournament(
            self,
            session: ClientSession,
            tournament_id: int,
            data: UpdateTournamentPartial
    ) -> Tournament:
        headers = await self.create_headers(session=session)
        async with session.get(
            self.api_urls.patch_tournament_by_id(tournament_id),
            headers=headers,
            json=data,
        ) as response:
            if response.status == 200:
                obj_dict = await response.json()
                return self._model.model_validate(obj_dict)
            if response.status == 422:
                raise ValidationError('Invalid tournament fields')
            raise HTTPError('Server error')

    async def delete_tournament(
            self,
            session: ClientSession,
            tournament_id: int
    ) -> str:
        headers = await self.create_headers(session=session)
        async with session.delete(
            self.api_urls.delete_tournament_by_id(tournament_id),
            headers=headers,
        ) as response:
            if response.status == 204:
                return await response.json()
            if response.status == 422:
                raise ValidationError('Invalid tournament id')
            raise HTTPError('Server error')

    async def get_tournament_by_name(
            self,
            session: ClientSession,
            name: str
    ) -> Tournament:
        headers = await self.create_headers(session=session)
        async with session.get(
            self.api_urls.get_tournament_by_name(name),
            headers=headers,
        ) as response:
            if response.status == 200:
                obj_dict = await response.json()
                return self._model.model_validate(obj_dict)
            if response.status == 422:
                raise ValidationError('Invalid tournament tg id')
            raise HTTPError('Server error')

    async def create_tournament(
            self,
            session: ClientSession,
            data: CreateTournament
    ) -> Tournament:
        headers = await self.create_headers(session=session)
        print(data)
        async with session.post(
            self.api_urls.post_tournament(),
            headers=headers,
            json=data,
        ) as response:
            if response.status == 201:
                obj_dict = await response.json()
                return self._model.model_validate(obj_dict)
            if response.status == 422:
                raise ValidationError('Invalid tournament fields')
            raise HTTPError('Server error')

    async def add_user_in_tournament(
            self,
            session: ClientSession,
            user_tg_id: int,
            tournament_id: int,
    ) -> Dict[str, Any]:
        headers = await self.create_headers(session=session)
        data = {
              "tournament_id": {
                "tournament_id": tournament_id
              },
              "user_tg_id": {
                "user_tg_id": user_tg_id
              }
            }
        async with session.post(
            self.api_urls.post_tournament_adduser(),
            headers=headers,
            json=data,
        ) as response:
            if response.status == 200:
                obj_dict = await response.json()
                return obj_dict
            if response.status == 422:
                raise ValidationError('Invalid tournament fields')
            raise HTTPError('Server error')



