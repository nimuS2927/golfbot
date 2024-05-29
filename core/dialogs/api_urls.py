from core.config import c_api


class ApiURL:
    _instance = None
    _base_url = c_api.base_url
    _prefix_login = c_api.prefix_login
    _prefix_db = c_api.prefix_db

    def __new__(cls):
        if not cls._instance:
            instance = super(ApiURL, cls).__new__(cls)
            cls._instance = instance
        return cls._instance

    def __init__(self):
        # region URL Admins
        self.__POST_ADMIN_BY_LOGIN = self._base_url + self._prefix_login + 'admins/authorization/'
        self.__POST_ADMIN = self._base_url + self._prefix_login + 'admins/'
        self.__POST_ADMIN_AUTHORIZATION_FOR_SUPERUSER = self._base_url + self._prefix_login + 'admins/authorization/'
        self.__POST_ADMIN = self._base_url + self._prefix_login + 'admins/'
        self.__DELETE_ADMIN_BY_LOGIN = self._base_url + self._prefix_login + 'admins/'
        # endregion
        # region URL tokens
        self.__POST_TOKENS = self._base_url + self._prefix_login + 'tokens/full/'
        self.__POST_REFRESH_ACCESS_TOKEN = self._base_url + self._prefix_login + 'tokens/access/'
        # endregion
        # region URL Users
        self.__GET_USERS = self._base_url + self._prefix_db + 'user/'
        self.__GET_USER_BY_ID = self._base_url + self._prefix_db + 'user/'
        self.__PUT_USER_BY_ID = self._base_url + self._prefix_db + 'user/'
        self.__PATCH_USER_BY_ID = self._base_url + self._prefix_db + 'user/'
        self.__DELETE_USER_BY_ID = self._base_url + self._prefix_db + 'user/'
        self.__GET_USER_BY_TG_ID = self._base_url + self._prefix_db + 'user/tg/'
        self.__POST_USER = self._base_url + self._prefix_db + 'user/'
        # endregion
        # region URL tournaments
        self.__GET_TOURNAMENTS = self._base_url + self._prefix_db + 'tournaments/'
        self.__GET_TOURNAMENTS_FOR_GAME = self._base_url + self._prefix_db + 'tournaments/game/'
        self.__POST_TOURNAMENT = self._base_url + self._prefix_db + 'tournaments/'
        self.__POST_TOURNAMENT_DISTRIBUTE = self._base_url + self._prefix_db + 'tournaments/distribute/'
        self.__POST_TOURNAMENT_ADDUSER = self._base_url + self._prefix_db + 'tournaments/adduser/'
        self.__GET_TOURNAMENT_BY_NAME = self._base_url + self._prefix_db + 'tournaments/name/'
        self.__GET_TOURNAMENT_BY_ID = self._base_url + self._prefix_db + 'tournaments/'
        self.__PUT_TOURNAMENT_BY_ID = self._base_url + self._prefix_db + 'tournaments/'
        self.__PATCH_TOURNAMENT_BY_ID = self._base_url + self._prefix_db + 'tournaments/'
        self.__DELETE_TOURNAMENT_BY_ID = self._base_url + self._prefix_db + 'tournaments/'
        self.__GET_TOURNAMENT_NEAREST = self._base_url + self._prefix_db + 'tournaments/nearest/'
        self.__POST_TOURNAMENT_NEAREST = self._base_url + self._prefix_db + 'tournaments/nearest/'
        # endregion
        # region URL Holes
        self.__GET_HOLES_BY_COURSE_ID = self._base_url + self._prefix_db + 'holes/course/'
        self.__GET_HOLE_BY_ID = self._base_url + self._prefix_db + 'holes/'
        self.__GET_HOLES = self._base_url + self._prefix_db + 'holes/'
        self.__GET_HOLE_BY_NUMBER = self._base_url + self._prefix_db + 'holes/number/'
        self.__POST_HOLE = self._base_url + self._prefix_db + 'holes/'
        self.__PUT_HOLE_BY_ID = self._base_url + self._prefix_db + 'holes/'
        self.__PATCH_HOLE_BY_ID = self._base_url + self._prefix_db + 'holes/'
        self.__DELETE_HOLE_BY_ID = self._base_url + self._prefix_db + 'holes/'
        # endregion
        # region URL Scores
        self.__GET_SCORES = self._base_url + self._prefix_db + 'scores/'
        self.__POST_SCORE = self._base_url + self._prefix_db + 'scores/'
        self.__POST_SCORES = self._base_url + self._prefix_db + 'scores/many/'
        self.__GET_SCORE_BY_ID = self._base_url + self._prefix_db + 'scores/'
        self.__PUT_SCORE_BY_ID = self._base_url + self._prefix_db + 'scores/'
        self.__PATCH_SCORE_BY_ID = self._base_url + self._prefix_db + 'scores/'
        self.__DELETE_SCORE_BY_ID = self._base_url + self._prefix_db + 'scores/'
        self.__GET_SCORES_BY_ID_TOURNAMENT_AND_ID_HOLE = self._base_url + self._prefix_db + 'scores/'
        self.__GET_SCORES_BY_ID_TOURNAMENT_AND_ID_USER = self._base_url + self._prefix_db + 'scores/'
        self.__GET_SCORE_BY_ID_TOURNAMENT = self._base_url + self._prefix_db + 'scores/tournament/'
        # endregion
        # region URL TotalScores
        self.__GET_TOTAL_SCORES = self._base_url + self._prefix_db + 'totalscore/'
        self.__POST_TOTAL_SCORE = self._base_url + self._prefix_db + 'totalscore/'
        self.__GET_TOTAL_SCORE_BY_ID = self._base_url + self._prefix_db + 'totalscore/'
        self.__PUT_TOTAL_SCORE_BY_ID = self._base_url + self._prefix_db + 'totalscore/'
        self.__PATCH_TOTAL_SCORE_BY_ID = self._base_url + self._prefix_db + 'totalscore/'
        self.__DELETE_TOTAL_SCORE_BY_ID = self._base_url + self._prefix_db + 'totalscore/'
        self.__GET_TOTAL_SCORE_BY_ID_TOURNAMENT_AND_ID_USER = self._base_url + self._prefix_db + 'totalscore/'
        self.__GET_TOTAL_SCORE_BY_ID_TOURNAMENT = self._base_url + self._prefix_db + 'scores/tournament/'

        # endregion

    # region Functions to getting URL settings
    # region to getting Admins
    def post_admin_by_login(self) -> str:
        return self.__POST_ADMIN_BY_LOGIN

    def post_admin(self) -> str:
        return self.__POST_ADMIN

    def post_admin_authorization_for_superuser(self, login) -> str:
        return self.__POST_ADMIN_AUTHORIZATION_FOR_SUPERUSER + login + '/'

    def delete_admin_by_login(self, login: str) -> str:
        return self.__DELETE_ADMIN_BY_LOGIN + login + '/'

    # endregion
    # region to getting tokens
    def post_tokens(self) -> str:
        return self.__POST_TOKENS

    def post_refresh_access_token(self) -> str:
        return self.__POST_REFRESH_ACCESS_TOKEN

    # endregion
    # region to getting Users
    def get_users(self) -> str:
        return self.__GET_USERS

    def get_user_by_id(self, user_id: int) -> str:
        return self.__GET_USER_BY_ID + str(user_id) + '/'

    def put_user_by_id(self, user_id: int) -> str:
        return self.__PUT_USER_BY_ID + str(user_id) + '/'

    def patch_user_by_id(self, user_id: int) -> str:
        return self.__PATCH_USER_BY_ID + str(user_id) + '/'

    def delete_user_by_id(self, user_id: int) -> str:
        return self.__DELETE_USER_BY_ID + str(user_id) + '/'

    def get_user_by_tg_id(self, tg_id: int) -> str:
        return self.__GET_USER_BY_TG_ID + str(tg_id) + '/'

    def post_user(self) -> str:
        return self.__POST_USER

    # endregion
    # region to getting Tournaments
    def get_tournaments(self) -> str:
        return self.__GET_TOURNAMENTS

    def get_tournaments_for_game(self, user_tg_id: int) -> str:
        return self.__GET_TOURNAMENTS_FOR_GAME + str(user_tg_id) + '/'

    def post_tournament(self) -> str:
        return self.__POST_TOURNAMENT

    def post_tournament_distribute(self) -> str:
        return self.__POST_TOURNAMENT_DISTRIBUTE

    def post_tournament_adduser(self) -> str:
        return self.__POST_TOURNAMENT_ADDUSER

    def get_tournament_by_id(self, tournament_id: int) -> str:
        return self.__GET_TOURNAMENT_BY_ID + str(tournament_id) + '/'

    def put_tournament_by_id(self, tournament_id: int) -> str:
        return self.__PUT_TOURNAMENT_BY_ID + str(tournament_id) + '/'

    def patch_tournament_by_id(self, tournament_id: int) -> str:
        return self.__PATCH_TOURNAMENT_BY_ID + str(tournament_id) + '/'

    def delete_tournament_by_id(self, tournament_id: int) -> str:
        return self.__DELETE_TOURNAMENT_BY_ID + str(tournament_id) + '/'

    def post_tournament_nearest(self) -> str:
        return self.__POST_TOURNAMENT_NEAREST

    def get_tournament_nearest(self) -> str:
        return self.__GET_TOURNAMENT_NEAREST

    def get_tournament_by_name(self, tournament_name: str) -> str:
        return self.__GET_TOURNAMENT_BY_NAME + tournament_name + '/'

    # endregion
    # region to getting Holes
    def get_holes_by_course_id(self, id_course: int) -> str:
        return self.__GET_HOLES_BY_COURSE_ID + str(id_course) + '/'

    def get_hole_by_id(self, hole_id: int) -> str:
        return self.__GET_HOLE_BY_ID + str(hole_id) + '/'

    def get_holes(self) -> str:
        return self.__GET_HOLES

    def get_hole_by_number(self, hole_number: int) -> str:
        return self.__GET_HOLE_BY_NUMBER + str(hole_number) + '/'

    def post_hole(self) -> str:
        return self.__POST_HOLE

    def put_hole_by_id(self, hole_id: int) -> str:
        return self.__PUT_HOLE_BY_ID + str(hole_id) + '/'

    def patch_hole_by_id(self, hole_id: int) -> str:
        return self.__PATCH_HOLE_BY_ID + str(hole_id) + '/'

    def delete_hole_by_id(self, hole_id: int) -> str:
        return self.__DELETE_HOLE_BY_ID + str(hole_id) + '/'

    # endregion
    # region to getting Scores
    def get_scores(self) -> str:
        return self.__GET_SCORES

    def post_score(self) -> str:
        return self.__POST_SCORE

    def post_scores(self) -> str:
        return self.__POST_SCORES

    def get_score_by_id(self, score_id: int) -> str:
        return self.__GET_SCORE_BY_ID + str(score_id) + '/'

    def put_score_by_id(self, score_id: int) -> str:
        return self.__PUT_SCORE_BY_ID + str(score_id) + '/'

    def patch_score_by_id(self, score_id: int) -> str:
        return self.__PATCH_SCORE_BY_ID + str(score_id) + '/'

    def delete_score_by_id(self, score_id: int) -> str:
        return self.__DELETE_SCORE_BY_ID + str(score_id) + '/'

    def get_score_by_id_tournament(self, id_tournament: int) -> str:
        return self.__GET_SCORE_BY_ID_TOURNAMENT + str(id_tournament) + '/'

    def get_scores_by_id_tournament_and_id_hole(self, id_tournament: int, id_hole: int) -> str:
        return self.__GET_SCORES_BY_ID_TOURNAMENT_AND_ID_HOLE + str(id_tournament) + '/hole/' + str(id_hole) + '/'

    def get_scores_by_id_tournament_and_id_user(self, id_tournament: int, id_user: int) -> str:
        return self.__GET_SCORES_BY_ID_TOURNAMENT_AND_ID_USER + str(id_tournament) + '/user/' + str(id_user) + '/'
    # endregion

    # region to getting Scores
    def get_totalscores(self) -> str:
        return self.__GET_TOTAL_SCORES

    def post_totalscore(self) -> str:
        return self.__POST_TOTAL_SCORE

    def get_totalscore_by_id(self, totalscore_id: int) -> str:
        return self.__GET_TOTAL_SCORE_BY_ID + str(totalscore_id) + '/'

    def put_totalscore_by_id(self, totalscore_id: int) -> str:
        return self.__PUT_TOTAL_SCORE_BY_ID + str(totalscore_id) + '/'

    def patch_totalscore_by_id(self, totalscore_id: int) -> str:
        return self.__PATCH_TOTAL_SCORE_BY_ID + str(totalscore_id) + '/'

    def delete_totalscore_by_id(self, totalscore_id: int) -> str:
        return self.__DELETE_TOTAL_SCORE_BY_ID + str(totalscore_id) + '/'

    def get_totalscores_by_id_tournament(self, id_tournament: int) -> str:
        return self.__GET_TOTAL_SCORE_BY_ID_TOURNAMENT + str(id_tournament) + '/'

    def get_totalscore_by_id_tournament_and_id_user(self, id_tournament: int, id_user: int) -> str:
        return self.__GET_TOTAL_SCORE_BY_ID_TOURNAMENT_AND_ID_USER + str(id_tournament) + '/user/' + str(id_user) + '/'
    # endregion
    # endregion


api_urls = ApiURL()
