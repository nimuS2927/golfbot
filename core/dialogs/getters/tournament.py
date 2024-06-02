import datetime
from typing import List

from aiogram_dialog import DialogManager
from aiohttp import ClientSession

from core.dialogs.utils.pluralization_rules import pluralization
from core.dialogs.schemas.tournaments import Tournament
from core.dialogs.services import TournamentService

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

    async def get_tournaments_for_game(
            self,
            dialog_manager: DialogManager,
            **middleware_data
    ):
        user_tg_id = dialog_manager.event.from_user.id
        middleware_data = dialog_manager.middleware_data
        session: ClientSession = middleware_data.get('session')
        objs: List[Object] = await self.service.get_tournaments_for_game(
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
        start = obj.start
        end = obj.end
        if isinstance(start, str):
            start_datetime = datetime.datetime.strptime(start, '%Y-%m-%dT%H:%M:%S')
            start = datetime.datetime.strftime(start_datetime, '%Y-%m-%d %H:%M')
        elif isinstance(start, datetime.datetime):
            start = datetime.datetime.strftime(start, '%Y-%m-%d %H:%M')
        if isinstance(end, str):
            end_datetime = datetime.datetime.strptime(end, '%Y-%m-%dT%H:%M:%S')
            end = datetime.datetime.strftime(end_datetime, '%Y-%m-%d %H:%M')
        elif isinstance(end, datetime.datetime):
            end = datetime.datetime.strftime(end, '%Y-%m-%d %H:%M')
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

    async def get_totalscores(
            self,
            dialog_manager: DialogManager,
            **middleware_data
    ):
        """ Get object by id """
        middleware_data = dialog_manager.middleware_data
        session = middleware_data.get('session')
        dialog_data = dialog_manager.dialog_data
        totalscores = dialog_data.get('totalscores')
        totalscores_list = []
        for totalscore in totalscores:
            first_name = totalscore['user']['first_name']
            last_name = totalscore['user']['last_name']
            holes_completed = 0
            count_impacts = 0
            for score in totalscore['scores']:
                if score['impacts']:
                    holes_completed += 1
                    count_impacts += score['impacts']
            total = totalscore['total']
            totalscores_list.append((first_name, last_name, count_impacts, holes_completed, total))
        tournament_type = dialog_data.get('tournament_type')
        result_list = []
        if tournament_type == 'stableford':
            result_list = sorted(totalscores_list, key=lambda x: x[-1], reverse=True)
        elif tournament_type == 'stroke play' or tournament_type == 'stroke play nett':
            result_list = sorted(totalscores_list, key=lambda x: x[-1])
        data = {
            'totalscores_list': result_list
        }
        return data

    @staticmethod
    async def get_impacts(
            dialog_manager: DialogManager,
            **middleware_data
    ):
        impacts_list = [(i, i) for i in range(1, 11)]
        data = {
            'impacts_list': impacts_list
        }
        dialog_manager.current_context().dialog_data.update(impacts_list=impacts_list)
        return data


g_tournament = TournamentGetter()
