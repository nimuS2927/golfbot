from aiogram_dialog import Window, Data, DialogManager, ShowMode, Dialog
from aiogram_dialog.widgets.kbd import Cancel, Back, Button, SwitchTo
from aiogram_dialog.widgets.text import Const, Format, List
from aiogram_dialog.widgets.media import StaticMedia, DynamicMedia
from aiogram_dialog.widgets.input import TextInput

from core.config import c_project

from core.main.keyboards.buttons import MainKB, RegistrationBotKB, RegistrationTournamentKB
from . import keyboards
from .selected import registration_bot, main_menu
from .selected import tournament as s_tournament
from core.dialogs.states import all_states
from core.dialogs.getters import get_registration_data, g_tournament


class AllWindows:

    @staticmethod
    def main_window():
        return Window(
            Const('Вас приветствует Бот гольф-клуба "Ваше название"! Выберите интересующий вас пункт...'),
            Button(
                Format(f'{MainKB.registration_bot[0]}'),
                id=MainKB.registration_bot[1],
                on_click=registration_bot.on_registration_bot,
            ),
            Button(
                Format(f'{MainKB.registration_tournament[0]}'),
                id=MainKB.registration_tournament[1],
                on_click=s_tournament.on_registration_tournament
            ),
            Cancel(Format(f'{MainKB.cancel[0]}')),
            state=all_states.main.start,
            # getter=[getters.get_emoji, getters.g_images.get_main]
        )

    # region Registration Bot
    @staticmethod
    def start_registration_bot_window():
        return Window(
            Format('''Начался процесс регистрации в нашем боте. 
Ваше имя: {first_name}
Ваша фамилия: {last_name}
Ваш номер телефона: {phone}
Ваш гандикап: {handicap}
            '''),
            SwitchTo(
                Format(f'{RegistrationBotKB.your_name[0]}'),
                id=RegistrationBotKB.your_name[1],
                state=all_states.registration_bot.first_name,
                # on_click=registration_bot.on_entered_first_name
            ),
            SwitchTo(
                Format(f'{RegistrationBotKB.your_surname[0]}'),
                id=RegistrationBotKB.your_surname[1],
                state=all_states.registration_bot.last_name,
                # on_click=registration_bot.on_entered_last_name
            ),
            SwitchTo(
                Format(f'{RegistrationBotKB.your_phone[0]}'),
                id=RegistrationBotKB.your_phone[1],
                state=all_states.registration_bot.phone,
                # on_click=registration_bot.on_entered_phone
            ),
            SwitchTo(
                Format(f'{RegistrationBotKB.your_handicap[0]}'),
                id=RegistrationBotKB.your_handicap[1],
                state=all_states.registration_bot.handicap,
                # on_click=registration_bot.on_entered_handicap
            ),
            Button(
                Format(f'{RegistrationBotKB.confirm[0]}'),
                id=RegistrationBotKB.confirm[1],
                on_click=registration_bot.on_entered_confirm
            ),
            Cancel(Format(f'{MainKB.cancel[0]}')),
            state=all_states.registration_bot.start,
            getter=get_registration_data
        )

    @staticmethod
    def entered_first_name_window():
        return Window(
            Const('Введите ваше имя:'),
            TextInput(
                id='first_name',
                on_success=registration_bot.on_entered_first_name
            ),
            state=all_states.registration_bot.first_name,
        )

    @staticmethod
    def entered_last_name_window():
        return Window(
            Const('Введите вашу фамилию:'),
            TextInput(
                id='last_name',
                on_success=registration_bot.on_entered_last_name
            ),
            state=all_states.registration_bot.last_name,
        )

    @staticmethod
    def entered_phone_window():
        return Window(
            Const('Введите ваш телефон:'),
            TextInput(
                id='phone',
                on_success=registration_bot.on_entered_phone
            ),
            state=all_states.registration_bot.phone,
        )

    @staticmethod
    def entered_handicap_window():
        return Window(
            Const('Введите ваш гандикап:'),
            TextInput(
                id='phone',
                on_success=registration_bot.on_entered_handicap
            ),
            state=all_states.registration_bot.handicap,
        )

    @staticmethod
    def end_registration_window():
        return Window(
            Format('''Поздравляю {dialog_data[last_name]} {dialog_data[first_name]}! 
Вы зарегистрированы в нашем боте.
Ваш текущий гандикап {dialog_data[handicap]}
                        '''),
            Button(
                Format(f'{MainKB.main_menu[0]}'),
                id=MainKB.main_menu[1],
                on_click=main_menu.on_main_menu,
            ),
            state=all_states.registration_bot.end,
        )
    # endregion

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
    # endregion

    # region Game

    # endregion


def all_dialogs():
    return [
        Dialog(
            AllWindows.main_window(),
        ),
        Dialog(
            AllWindows.start_registration_bot_window(),
            AllWindows.entered_first_name_window(),
            AllWindows.entered_last_name_window(),
            AllWindows.entered_phone_window(),
            AllWindows.entered_handicap_window(),
            AllWindows.end_registration_window(),
        ),
        Dialog(
            AllWindows.start_registration_tournament_window(),
            AllWindows.info_registration_tournament_window(),
            AllWindows.end_registration_tournament_window(),
            AllWindows.empty_registration_tournament_window(),
        ),
    ]

