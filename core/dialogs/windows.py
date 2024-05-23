import os.path
from pathlib import Path

from aiogram_dialog import Window, Data, DialogManager, ShowMode, Dialog
from aiogram_dialog.widgets.kbd import Cancel, Back, Button, SwitchTo
from aiogram_dialog.widgets.text import Const, Format, List
from aiogram_dialog.widgets.media import StaticMedia, DynamicMedia
from aiogram_dialog.widgets.input import TextInput

from core.config import c_project
# from core.dialogs.main_menu import keyboards, states, selected
from aiogram.types import ContentType

from core.main.keyboards.buttons import MainKB, RegistrationBotKB
from .selected import registration_bot, registration_tournament, main_menu
from core.dialogs.states import all_states
from core.dialogs.getters import get_registration_data


class AllWindows:

    @staticmethod
    def main_window():
        return Window(
            Const('Вас приветствует Бот гольф-клуба "Ваше название"! Выберите интересующий вас пункт...'),
            SwitchTo(
                Format(f'{MainKB.registration_bot[0]}'),
                id=MainKB.registration_bot[1],
                state=all_states.registration_bot.start,
                on_click=registration_bot.on_registration_bot,
            ),
            SwitchTo(
                Format(f'{MainKB.registration_tournament[0]}'),
                id=MainKB.registration_tournament[1],
                state=all_states.registration_tournament.start,
                on_click=registration_tournament.on_registration_tournament
            ),
            Cancel(Format(f'{MainKB.cancel[0]}')),
            state=all_states.main.start,
            # getter=[getters.get_emoji, getters.g_images.get_main]
        )

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
    ]

