from typing import List, Optional, Dict

from aiogram_dialog import DialogManager
from aiohttp import ClientSession

from core.dialogs.schemas.scores import Score
from core.dialogs.utils import getters_obj_from_list, emoji
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
        # region Получаем контекст и переменные
        context = dialog_manager.current_context()
        holes_ids: Optional[Dict[int, list[int, int, int, str]]] = context.dialog_data.get('holes_ids')
        scores_dict: List[dict] = context.dialog_data.get('scores')
        scores: List[Score] = [Score.model_validate(i_dict) for i_dict in scores_dict]
        holes_dict: List[dict] = context.dialog_data.get('holes')
        holes: List[Hole] = [Hole.model_validate(i_dict) for i_dict in holes_dict]
        # endregion
        # region Когда в данных диалога нет заполненных лунок, проверяем данные полученные из базы
        if not holes_ids:
            holes_ids = {}
            for sc in scores:
                if sc.impacts:
                    hole: Hole = getters_obj_from_list.get_obj_by_attribute(
                        objs=holes,
                        attribute='id',
                        value=sc.id_hole
                    )
                    holes_ids[hole.id] = [
                        sc.impacts,
                        hole.par,
                        hole.difficulty,
                        emoji.for_holes(sc.impacts - hole.par)
                    ]
        # endregion
        # region Формируем данные для кнопок (лунок)
        holes_list = [
            (hole.id, hole.number, hole.par, '○')
            if hole.id not in holes_ids.keys()
            else (hole.id, hole.number, hole.par, holes_ids[hole.id][3])
            for hole in holes]
        data = {
            'holes_list': holes_list,
        }
        # endregion
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
