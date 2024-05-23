from aiogram.fsm.state import StatesGroup, State


class MainMenuState(StatesGroup):
    start = State()


class RegistrationBot(StatesGroup):
    start = State()
    first_name = State()
    last_name = State()
    phone = State()
    handicap = State()
    confirm = State()
    end = State()


class RegistrationTournament(StatesGroup):
    start = State()
    info = State()


class AllStates:
    def __init__(self):
        self.main = MainMenuState()
        self.registration_bot = RegistrationBot()
        self.registration_tournament = RegistrationTournament()


all_states = AllStates()
