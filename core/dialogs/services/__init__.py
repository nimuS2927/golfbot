__all__ = {
    'all_services',
    'UserService',
    'TournamentService',
    'HoleService',
    'ScoreService',
    'TotalScoreService',
}

from core.dialogs.services.users import UserService
from core.dialogs.services.tournaments import TournamentService
from core.dialogs.services.holes import HoleService
from core.dialogs.services.scores import ScoreService
from core.dialogs.services.totalscores import TotalScoreService


class AllServices:
    def __init__(self):
        self.__user = UserService()
        self.__tournament = TournamentService()
        self.__hole = HoleService()
        self.__score = ScoreService()
        self.__totalscores = TotalScoreService()

    # region get services
    @property
    def user(self):
        return self.__user

    @property
    def tournament(self):
        return self.__tournament

    @property
    def hole(self):
        return self.__hole

    @property
    def score(self):
        return self.__score

    @property
    def totalscores(self):
        return self.__totalscores
    # endregion


all_services = AllServices()
