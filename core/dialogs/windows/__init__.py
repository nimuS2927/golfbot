__all__ = [
    'all_dialogs',
]

from .game import GameWindows
from .registration_bot import RegistrationBotWindows
from .registration_tournament import RegistrationTournamentWindows
from .main_menu import MainMenuWindow
from .admins import AdminWindows

from aiogram_dialog import Dialog


def all_dialogs():
    return [
        Dialog(
            MainMenuWindow.main_window(),
        ),
        Dialog(
            RegistrationBotWindows.start_registration_bot_window(),
            RegistrationBotWindows.run_registration_bot_window(),
            RegistrationBotWindows.entered_first_name_window(),
            RegistrationBotWindows.entered_last_name_window(),
            RegistrationBotWindows.entered_phone_window(),
            RegistrationBotWindows.entered_handicap_window(),
            RegistrationBotWindows.end_registration_window(),
        ),
        Dialog(
            RegistrationTournamentWindows.start_registration_tournament_window(),
            RegistrationTournamentWindows.info_registration_tournament_window(),
            RegistrationTournamentWindows.end_registration_tournament_window(),
            RegistrationTournamentWindows.anonymous_registration_tournament_window(),
            RegistrationTournamentWindows.empty_registration_tournament_window(),
        ),
        Dialog(
            GameWindows.choice_game_window(),
            GameWindows.start_game_window(),
            GameWindows.empty_game_window(),
            GameWindows.entered_impacts_window(),
            GameWindows.empty_hole_game_window(),
            GameWindows.end_game_window(),
        ),
    ]