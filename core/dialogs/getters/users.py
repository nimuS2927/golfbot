from aiogram_dialog import DialogManager

from core.dialogs.utils.pluralization_rules import pluralization
from core.dialogs.schemas.users import User
from core.dialogs.services import UserService


Object = User


class UserGetter:

    def __init__(self):
        self.service = UserService()
        self.__singular = 'user'
        self.__plural = pluralization(self.singular)

    @property
    def singular(self):
        return self.__singular

    @property
    def plural(self):
        return self.__plural

    async def get_one(
            self,
            dialog_manager: DialogManager,
            **middleware_data
    ):
        """ Get object by id """
        middleware_data = dialog_manager.middleware_data
        session = middleware_data.get('session')
        dialog_data = dialog_manager.dialog_data
        obj_id: int = dialog_data.get(self.singular + '_id')
        obj: Object = await self.service.get_user(session=session, user_id=obj_id)
        data = {
            self.singular: obj
        }
        return data

    async def get_user_by_tg_id(
            self,
            dialog_manager: DialogManager,
            **middleware_data
    ):
        middleware_data = dialog_manager.middleware_data
        session = middleware_data.get('session')
        dialog_data = dialog_manager.dialog_data
        tg_id: int = dialog_data.get('tg_id')
        obj: Object = await self.service.get_user_by_tg_id(session=session, tg_id=tg_id)
        data = {
            self.singular: obj
        }
        return data


g_user = UserGetter()
