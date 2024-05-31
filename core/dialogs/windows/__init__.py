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
        Dialog(
            AdminWindows.authorization_window(),
            AdminWindows.forbidden_window(),
            AdminWindows.admin_window(),
            AdminWindows.show_tournament_window(),
            AdminWindows.choice_tournament_window(),
            AdminWindows.info_tournament_window(),
            AdminWindows.delete_tournament_window(),
            AdminWindows.edit_tournament_window(),
            AdminWindows.entered_name_window(),
            AdminWindows.entered_type_window(),
            AdminWindows.entered_flights_window(),
            AdminWindows.entered_course_name_window(),
            AdminWindows.entered_start_window(),
            AdminWindows.entered_end_window(),
            AdminWindows.entered_hcp_window(),
            AdminWindows.choice_user_window(),
            AdminWindows.info_user_window(),
            AdminWindows.delete_user_window(),
            AdminWindows.entered_handicap_window(),
        ),
    ]
