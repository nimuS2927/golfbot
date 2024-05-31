from aiogram.fsm.state import StatesGroup, State


class MainMenuState(StatesGroup):
    start = State()


class RegistrationBot(StatesGroup):
    start = State()
    run = State()
    first_name = State()
    last_name = State()
    phone = State()
    handicap = State()
    confirm = State()
    end = State()


class RegistrationTournament(StatesGroup):
    start = State()
    info = State()
    empty = State()
    end = State()
    anonymous = State()


class Game(StatesGroup):
    choice = State()
    start = State()
    result = State()
    empty = State()
    empty_holes = State()
    end = State()


class Admin(StatesGroup):
    authorization = State()
    forbidden = State()
    start = State()
    # region Tournaments
    show_tournaments = State()
    choice_tournament = State()
    info_tournament = State()
    edit_tournament = State()
    create_tournament = State()
    delete_tournament = State()
    entered_name = State()
    entered_type = State()
    entered_flights = State()
    entered_course_name = State()
    entered_start = State()
    entered_end = State()
    entered_hcp = State()
    # endregion Tournaments
    # region Users
    show_users = State()
    info_user = State()
    entered_handicap = State()
    delete_user = State()
    # endregion Users
    # region Admins
    show_admins = State()
    delete_admin = State()
    # endregion Admins
    # region Courses
    show_courses = State()
    edit_course = State()
    create_course = State()
    delete_course = State()
    # endregion Courses


class AllStates:
    def __init__(self):
        self.main = MainMenuState()
        self.registration_bot = RegistrationBot()
        self.registration_tournament = RegistrationTournament()
        self.game = Game()
        self.admin = Admin()


all_states = AllStates()
