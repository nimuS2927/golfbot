from typing import List

from aiogram_dialog import DialogManager
from aiohttp import ClientSession

from core.config import c_project
from core.dialogs.pluralization_rules import pluralization
from core.dialogs.schemas.tournaments import Tournament
from core.dialogs.services import TournamentService
from core.dialogs.states import all_states

Object = Tournament


class TournamentGetter:

    def __init__(self):
        self.service = TournamentService()
        self.__singular = 'tournament'
        self.__plural = pluralization(self.singular)

    @property
    def singular(self):
        return self.__singular

    @property
    def plural(self):
        return self.__plural

    async def get_many(
            self,
            dialog_manager: DialogManager,
            **middleware_data
    ):
        """ Get all the objects """
        middleware_data = dialog_manager.middleware_data
        session: ClientSession = middleware_data.get('session')
        objs: List[Object] = await self.service.get_tournaments_all(session=session)
        data = {
            self.plural + '_all': objs
        }
        return data

    async def get_nearest(
            self,
            dialog_manager: DialogManager,
            **middleware_data
    ):
        """ Get the objects till 30 days from today """
        middleware_data = dialog_manager.middleware_data
        session: ClientSession = middleware_data.get('session')
        objs: List[Object] = await self.service.get_tournament_nearest(session=session)
        data = {
            self.plural: objs
        }
        return data

    async def get_nearest_without_user(
            self,
            dialog_manager: DialogManager,
            **middleware_data
    ):
        """ Get the objects till 30 days from today """
        user_tg_id = dialog_manager.event.from_user.id
        middleware_data = dialog_manager.middleware_data
        session: ClientSession = middleware_data.get('session')
        objs: List[Object] = await self.service.get_tournament_nearest_without_users(
            session=session,
            user_tg_id=user_tg_id
        )

        data = {
            self.plural: objs
        }
        return data

    async def get_one_by_id(
            self,
            dialog_manager: DialogManager,
            **middleware_data
    ):
        """ Get object by id """
        middleware_data = dialog_manager.middleware_data
        session = middleware_data.get('session')
        dialog_data = dialog_manager.dialog_data
        obj_id: int = dialog_data.get(self.singular + '_id')
        obj: Object = await self.service.get_tournament_by_id(session=session, tournament_id=obj_id)
        start = obj.start.strftime('%Y-%m-%d')
        end = obj.end.strftime('%Y-%m-%d')
        obj.start = start
        obj.end = end
        data = {
            self.singular: obj
        }
        return data

    async def get_one_by_name(
            self,
            dialog_manager: DialogManager,
            **middleware_data
    ):
        """ Get object by id """
        middleware_data = dialog_manager.middleware_data
        session = middleware_data.get('session')
        dialog_data = dialog_manager.dialog_data
        obj_name: str = dialog_data.get(self.singular + '_name')
        obj: Object = await self.service.get_tournament_by_name(session=session, name=obj_name)
        data = {
            self.singular: obj
        }
        return data


g_tournament = TournamentGetter()
