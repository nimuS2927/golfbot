__all__ = {
    'all_services',
    'UserService',
    'TournamentService',
    'HoleService',
    'ScoreService',
    'TotalScoreService',
    'AdminService',
    'CourseService',
}

from core.dialogs.services.users import UserService
from core.dialogs.services.tournaments import TournamentService
from core.dialogs.services.holes import HoleService
from core.dialogs.services.scores import ScoreService
from core.dialogs.services.totalscores import TotalScoreService
from core.dialogs.services.admins import AdminService
from core.dialogs.services.course import CourseService


class AllServices:
    def __init__(self):
        self.__user = UserService()
        self.__tournament = TournamentService()
        self.__hole = HoleService()
        self.__score = ScoreService()
        self.__totalscores = TotalScoreService()
        self.__admin = AdminService()
        self.__course = CourseService()

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

    @property
    def admin(self):
        return self.__admin

    @property
    def course(self):
        return self.__course
    # endregion


all_services = AllServices()
