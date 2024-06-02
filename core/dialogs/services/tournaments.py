import asyncio
import logging
from typing import Dict, Union, List, Any, Optional

from aiohttp import ClientSession
from pydantic import ValidationError
from requests import HTTPError

from core.dialogs.schemas.courses import Course
from core.dialogs.schemas.tournaments import Tournament, CreateTournament, UpdateTournament, UpdateTournamentPartial, \
    TournamentWithCourse
from core.dialogs.services.base import BaseService


logger = logging.getLogger(__name__)


class TournamentService(BaseService):
    _model = Tournament

    async def get_tournament_by_id(
            self,
            session: ClientSession,
            tournament_id: int,
            course_status: bool = False
    ) -> Optional[Union[Tournament, TournamentWithCourse]]:
        headers = await self.create_headers(session=session)
        async with session.get(
            self.api_urls.get_tournament_by_id(tournament_id, course_status),
            headers=headers,
        ) as response:
            if response.status == 200:
                obj_dict = await response.json()
                if course_status:
                    course: Course = Course.model_validate(obj_dict['course'])
                    obj_dict['course'] = course
                    return TournamentWithCourse.model_validate(obj_dict)
                else:
                    return Tournament.model_validate(obj_dict)
            elif response.status == 404:
                return None
            elif response.status == 422:
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
            elif response.status == 404:
                return []
            elif response.status == 422:
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
            if response.status == 404:
                return []
            if response.status == 422:
                raise ValidationError('Invalid request')
            raise HTTPError('Server error')

    async def get_tournaments_for_game(
            self,
            user_tg_id: int,
            session: ClientSession,
    ) -> List[Tournament]:

        logger.debug('get_tournaments_for_game')
        headers = await self.create_headers(session=session)

        async with session.get(
            self.api_urls.get_tournaments_for_game(user_tg_id=user_tg_id),
            headers=headers,
        ) as response:
            logger.debug('get requests for tournament')

            if response.status == 200:
                objs_dict = await response.json()
                logger.debug("successful requests for tournament")
                return [self._model.model_validate(dict_data) for dict_data in objs_dict]
            if response.status == 404:
                logger.debug("successful requests for tournament (NOT FOUND)")
                return []
            if response.status == 422:
                logger.debug("fail requests for tournament")
                raise ValidationError('Invalid request')
            logger.debug("other error after requests for tournament")
            raise HTTPError('Server error')

    async def update_tournament(
            self,
            session: ClientSession,
            tournament_id: int,
            data: UpdateTournament
    ) -> Tournament:
        headers = await self.create_headers(session=session)
        print(data)
        async with session.put(
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
        print('-' * 50)
        print(data)
        async with session.patch(
            self.api_urls.patch_tournament_by_id(tournament_id),
            headers=headers,
            json=data.model_dump(exclude_unset=True, exclude_none=True),
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
        async with session.post(
            self.api_urls.post_tournament(),
            headers=headers,
            json=data.model_dump(),
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

    async def distributed_users_in_tournament(
            self,
            session: ClientSession,
            tournament_id: int,
    ) -> Dict[str, Any]:
        headers = await self.create_headers(session=session)
        data = {'tournament_id': tournament_id}
        async with session.post(
                self.api_urls.post_tournament_distribute(),
                headers=headers,
                json=data,
        ) as response:
            if response.status == 200:
                obj_dict = await response.json()
                logger.debug("successful requests for tournament")
                return obj_dict
            if response.status == 404:
                logger.debug("successful requests for tournament (NOT FOUND)")
                return {}
            if response.status == 422:
                logger.debug("fail requests for tournament")
                raise ValidationError('Invalid request')
            logger.debug("other error after requests for tournament")
            raise HTTPError('Server error')

    async def get_tournament_for_top(
            self,
            session: ClientSession,
            tournament_id: int,
    ) -> Optional[Dict[str, Any]]:
        headers = await self.create_headers(session=session)
        async with session.get(
            self.api_urls.get_tournaments_for_top(tournament_id),
            headers=headers,
        ) as response:
            if response.status == 200:
                obj_dict = await response.json()
                return obj_dict
            elif response.status == 404:
                return None
            elif response.status == 422:
                raise ValidationError('Invalid tournament id')
            raise HTTPError('Server error')