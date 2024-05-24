__all__ = {
    'all_services',
    'UserService',
    'TournamentService',
}

from core.dialogs.services.users import UserService
from core.dialogs.services.tournaments import TournamentService


class AllServices:
    def __init__(self):
        self.__user = UserService()
        self.__tournament = TournamentService()

    # region get services
    @property
    def user(self):
        return self.__user

    @property
    def tournament(self):
        return self.__tournament
    # endregion


all_services = AllServices()
