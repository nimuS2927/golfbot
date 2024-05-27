"""
This config file is based on the principle of interaction between
environment variables and the singleton classes for their convenient use.

To use them you can import standard classes or initialize them with your names
  -- c_basic - ConfigBasic includes path to the project root folder (__PROJECT_DIR),
          path to the folder for storing temporary files (__PATH_TO_FILES),
          path to the folder for storing fixtures (__PATH_TO_FIXTURES)
  -- c_bot - ConfigBot includes access token for telegram bot (__TOKEN)
  -- c_project - ConfigProject includes all of the above.

    Property functions are defined for all parameters in the classes.
    In the classes BasicSettings, ConfigBot and ConfigDB, the names of these methods are equal
    to the names of the parameters in lowercase letters without the prefix __
    For the ConfigProject class use the prefix settings_ and name (bot or db or basic)
"""

import os
from pathlib import Path
from typing import List, Union, Optional, Type

from dotenv import load_dotenv, find_dotenv
from dataclasses import dataclass

load_dotenv(find_dotenv())


class ConfigBasic(object):
    _instance = None

    def __new__(cls):
        if not cls._instance:
            instance = super(ConfigBasic, cls).__new__(cls)
            cls._instance = instance
        return cls._instance

    def __init__(self):
        self.__PROJECT_DIR: Path = Path(__file__).parent.parent
        self.__PATH_TO_FILES: Path = Path.joinpath(self.__PROJECT_DIR, 'library', 'files')
        self.__PATH_TO_FILES.mkdir(parents=True, exist_ok=True)
        self.__PATH_TO_FIXTURES: Path = Path.joinpath(self.__PROJECT_DIR, 'library', 'fixtures')
        self.__PATH_TO_FIXTURES.mkdir(parents=True, exist_ok=True)
        self.__PATH_TO_IMAGES: Path = Path.joinpath(self.__PROJECT_DIR, 'library', 'images')
        self.__PATH_TO_IMAGES.mkdir(parents=True, exist_ok=True)
        self.__PATH_TO_LOGGING: Path = Path.joinpath(self.__PROJECT_DIR, 'library', 'logging')
        self.__PATH_TO_LOGGING.mkdir(parents=True, exist_ok=True)

    # region Functions to getting basic settings
    @property
    def project_dir(self) -> Path:
        return self.__PROJECT_DIR

    @property
    def path_to_files(self) -> Path:
        return self.__PATH_TO_FILES

    @property
    def path_to_fixtures(self) -> Path:
        return self.__PATH_TO_FIXTURES

    @property
    def path_to_images(self) -> Path:
        return self.__PATH_TO_IMAGES

    @property
    def path_to_logging(self) -> Path:
        return self.__PATH_TO_LOGGING
    # endregion


c_basic = ConfigBasic()


class ConfigBot(object):
    _instance = None

    def __new__(cls):
        if not cls._instance:
            instance = super(ConfigBot, cls).__new__(cls)
            cls._instance = instance
        return cls._instance

    def __init__(self):
        self.__TOKEN = os.getenv("TOKEN")
        self.__ADMIN_ID = os.getenv("ADMIN_ID")
        self.__ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

    # region Functions to getting bot settings
    @property
    def token(self) -> str:
        return self.__TOKEN

    @property
    def admin_id(self) -> str:
        return self.__ADMIN_ID

    @property
    def admin_password(self) -> str:
        return self.__ADMIN_PASSWORD
    # endregion


c_bot = ConfigBot()


class ConfigAPI(object):
    _instance = None

    def __new__(cls):
        if not cls._instance:
            instance = super(ConfigAPI, cls).__new__(cls)
            cls._instance = instance
        return cls._instance

    def __init__(self):
        self.__login_superuser = os.getenv("AUTH_SUPERUSER")
        self.__password_superuser = os.getenv("AUTH_PASSWORD")
        self.__base_url = os.getenv("BASE_URL", 'http://127.0.0.1:8000/')
        self.__prefix_login = os.getenv("PREFIX_LOGIN", 'auth/v1/')
        self.__prefix_db = os.getenv("PREFIX_DB", 'api/v1/')

    # region Functions to getting api settings
    @property
    def login_superuser(self):
        return self.__login_superuser

    @property
    def password_superuser(self):
        return self.__password_superuser

    @property
    def base_url(self):
        return self.__base_url

    @property
    def prefix_login(self):
        return self.__prefix_login

    @property
    def prefix_db(self):
        return self.__prefix_db
    # endregion


c_api = ConfigAPI()


class ConfigProject(object):
    _instance = None

    def __new__(cls):
        if not cls._instance:
            instance = super(ConfigProject, cls).__new__(cls)
            cls._instance = instance
        return cls._instance

    def __init__(self):
        self.__bot = c_bot
        # self.__db = c_db
        self.__basic = c_basic
        self.__api = c_api

    # region Functions to getting project settings
    @property
    def bot(self) -> ConfigBot:
        return self.__bot

    # @property
    # def db(self) -> ConfigDB:
    #     return self.__db

    @property
    def basic(self) -> ConfigBasic:
        return self.__basic

    @property
    def api(self):
        return self.__api
    # endregion


c_project = ConfigProject()
