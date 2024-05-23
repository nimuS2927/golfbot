__all__ = {
    'all_services',
    'UserService',
}

from core.dialogs.services.users import UserService


class AllServices:
    def __init__(self):
        self.__user = UserService()

    # region get services
    @property
    def user(self):
        return self.__user
    # endregion


all_services = AllServices()
