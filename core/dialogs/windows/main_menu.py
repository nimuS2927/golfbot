from aiogram_dialog import Window, Data, DialogManager, ShowMode, Dialog
from aiogram_dialog.widgets.kbd import Cancel, Back, Button, SwitchTo
from aiogram_dialog.widgets.text import Const, Format, List
from aiogram_dialog.widgets.media import StaticMedia, DynamicMedia
from aiogram_dialog.widgets.input import TextInput
from aiogram.types import CallbackQuery, Message

from core.config import c_project

from core.main.keyboards.buttons import MainKB, RegistrationBotKB, RegistrationTournamentKB, GameKB
from core.dialogs import keyboards
from core.dialogs.selected import registration_bot, main_menu
from core.dialogs.selected import tournament as s_tournament
from core.dialogs.selected import game as s_game
from core.dialogs.states import all_states
from core.dialogs.getters import get_registration_data, g_tournament, g_hole


async def on_close_bot(
        callback: CallbackQuery,
        button: Button,
        manager: DialogManager,
):
    await callback.message.answer('Всего доброго!')
    await manager.done()


class MainMenuWindow:

    @staticmethod
    def main_window():
        return Window(
            Const('Вас приветствует Бот гольф-клуба "Ваше название"! Выберите интересующий вас пункт...'),
            Button(
                Format(f'{MainKB.registration_tournament[0]}'),
                id=MainKB.registration_tournament[1],
                on_click=s_tournament.on_registration_tournament
            ),
            Button(
                Format(f'{GameKB.list_available_tournament[0]}'),
                id=GameKB.list_available_tournament[1],
                on_click=s_game.on_list_available_tournament
            ),
            Button(
                Format(f'{MainKB.cancel[0]}'),
                id=MainKB.cancel[1],
                on_click=on_close_bot
            ),
            state=all_states.main.start,
            # getter=[getters.get_emoji, getters.g_images.get_main]
        )
