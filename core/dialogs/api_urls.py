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
        self.__GET_ADMIN_BY_LOGIN = self._base_url + self._prefix_login + 'admins/'
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

    # region Functions to getting URL settings
    # region to getting Admins
    def get_admin_by_login(self) -> str:
        return self.__GET_ADMIN_BY_LOGIN

    def post_admin(self) -> str:
        return self.__POST_ADMIN

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
    # endregion


api_urls = ApiURL()
