from typing import List

from aiogram_dialog import DialogManager
from aiohttp import ClientSession

from core.dialogs.utils.pluralization_rules import pluralization
from core.dialogs.schemas.holes import Hole
from core.dialogs.services import HoleService

Object = Hole


class HoleGetter:

    def __init__(self):
        self.service = HoleService()
        self.__singular = 'hole'
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
        objs: List[Object] = await self.service.get_holes_all(session=session)
        data = {
            self.plural + '_all': objs
        }
        return data

    async def get_holes_by_course_id(
            self,
            dialog_manager: DialogManager,
            **middleware_data
    ):
        context = dialog_manager.current_context()
        user_tg_id = dialog_manager.event.from_user.id
        middleware_data = dialog_manager.middleware_data
        session: ClientSession = middleware_data.get('session')
        dialog_data = dialog_manager.dialog_data
        holes_ids = dialog_data.get('holes_ids')
        if not holes_ids:
            holes_ids = {}
        # tournament_id: int = dialog_data.get('tournament_id')
        # tournament: Tournament = await all_services.tournament.get_tournament_by_id(
        #     session=session,
        #     tournament_id=tournament_id
        # )
        # tournament: Optional[Tournament] = context.dialog_data.get('tournament')
        holes: List[Hole] = context.dialog_data.get('holes')
        # holes: List[Object] = await self.service.get_holes_by_course_id(
        #     session=session,
        #     course_id=tournament.id_course
        # )
        # context.dialog_data.update(holes=holes)
        holes_list = [(hole.id, hole.number, hole.par, '○') if hole.id not in holes_ids.keys() else (hole.id, hole.number, hole.par, '◉') for hole in holes ]
        data = {
            'holes_list': holes_list,
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
        obj: Object = await self.service.get_hole_by_id(session=session, hole_id=obj_id)
        data = {
            self.singular: obj
        }
        return data

    async def get_one_by_number(
            self,
            dialog_manager: DialogManager,
            **middleware_data
    ):
        """ Get object by id """
        middleware_data = dialog_manager.middleware_data
        session = middleware_data.get('session')
        dialog_data = dialog_manager.dialog_data
        obj_number: int = dialog_data.get(self.singular + '_number')
        obj: Object = await self.service.get_hole_by_number(session=session, number=obj_number)
        data = {
            self.singular: obj
        }
        return data

    @staticmethod
    async def get_empty_holes(
            dialog_manager: DialogManager,
            **middleware_data
    ):
        context = dialog_manager.current_context()
        empty_holes = context.dialog_data.get('empty_holes')
        data = {
            'empty_holes': empty_holes
        }
        return data


g_hole = HoleGetter()
