from aiogram_dialog import Window, Data, DialogManager, ShowMode, Dialog
from aiogram_dialog.widgets.kbd import Cancel, Back, Button, SwitchTo
from aiogram_dialog.widgets.text import Const, Format, List
from aiogram_dialog.widgets.media import StaticMedia, DynamicMedia
from aiogram_dialog.widgets.input import TextInput

from core.config import c_project

from core.main.keyboards.buttons import MainKB, RegistrationBotKB, RegistrationTournamentKB, GameKB
from core.dialogs import keyboards
from core.dialogs.selected import registration_bot, main_menu
from core.dialogs.selected import tournament as s_tournament
from core.dialogs.selected import game as s_game
from core.dialogs.states import all_states
from core.dialogs.getters import get_registration_data, g_tournament, g_hole


class RegistrationTournamentWindows:

    # region Registration tournament
    @staticmethod
    def start_registration_tournament_window():
        return Window(
            Format('Выберите турнир в котором хотите участвовать'),
            keyboards.paginated_tournaments(
                on_click=s_tournament.on_choice_tournament,
                width=1,
                height=5,
            ),
            Back(Format(f'{MainKB.back[0]}')),
            state=all_states.registration_tournament.start,
            getter=g_tournament.get_nearest_without_user
        )

    @staticmethod
    def empty_registration_tournament_window():
        return Window(
            Format('К сожалению для вас нет подходящего турнира в ближайшие 30 дней'),
            Cancel(Format(f'{MainKB.cancel[0]}')),
            state=all_states.registration_tournament.empty,
        )

    @staticmethod
    def info_registration_tournament_window():
        return Window(
            Format('''Турнир "{tournament.name}".
Стартует {tournament.start} и заканчивается {tournament.end}.
Максимальное число флайтов {tournament.max_flights}.
Тип турнира {tournament.types}
HCP = {tournament.hcp}
                        '''),
            Button(
                Format(f'{RegistrationTournamentKB.confirm[0]}'),
                id=RegistrationTournamentKB.confirm[1],
                on_click=s_tournament.on_entered_confirm
            ),
            Cancel(Format(f'{MainKB.cancel[0]}')),
            state=all_states.registration_tournament.info,
            getter=g_tournament.get_one_by_id
        )

    @staticmethod
    def end_registration_tournament_window():
        return Window(
            Format('''Поздравляю вы зарегистрированы в турнире!'''),
            Button(
                Format(f'{MainKB.main_menu[0]}'),
                id=MainKB.main_menu[1],
                on_click=main_menu.on_main_menu,
            ),
            state=all_states.registration_tournament.end,
        )

    @staticmethod
    def anonymous_registration_tournament_window():
        return Window(
            Const('Вы не зарегистрированный пользователь, вам не доступна эта функция!'),
            Cancel(Format(f'{MainKB.cancel[0]}')),
            state=all_states.registration_tournament.anonymous,
        )
    # endregion

