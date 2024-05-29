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
from core.dialogs.utils import emoji


class GameWindows:

    # region Game
    @staticmethod
    def choice_game_window():
        return Window(
            Format('Выберите турнир для запуска игры'),
            keyboards.paginated_tournaments(
                on_click=s_game.on_choice_tournament,
                width=1,
                height=5,
            ),
            Back(Format(f'{MainKB.back[0]}')),
            state=all_states.game.choice,
            getter=g_tournament.get_tournaments_for_game
        )

    @staticmethod
    def start_game_window():
        return Window(
            Format('''Игра началась! Вам необходимо заполнить число ударов на этих лунках...
Текущее количество очков: {dialog_data[total_score].total}
* Лунки указаны в формате "№ лунки (пар)"
* Символы (кол-во ударов от пара): (+2 {emoji[2]})  (+1 {emoji[1]})  (0 {emoji[0]})  (-1 {emoji[5]})  (-2 {emoji[4]})  (-3 {emoji[3]})
    '''),
            keyboards.paginated_holes(
                on_click=s_game.on_choice_holes,
                width=3,
                height=3,
            ),
            Button(
                Format(f'{GameKB.completed_game[0]}'),
                id=GameKB.completed_game[1],
                on_click=s_game.on_completed_game
            ),
            state=all_states.game.start,
            getter=[g_hole.get_holes_by_course_id, emoji.get_emoji]
        )

    @staticmethod
    def entered_impacts_window():
        return Window(
            Const('Введите количество совершенных ударов:'),
            TextInput(
                id='impacts',
                on_success=s_game.on_entered_impacts
            ),
            state=all_states.game.result,
        )

    @staticmethod
    def empty_game_window():
        return Window(
            Const('На текущий момент для вас нет доступных турниров для участия'),
            Cancel(Format(f'{MainKB.cancel[0]}')),
            state=all_states.game.empty,
        )

    @staticmethod
    def empty_hole_game_window():
        return Window(
            Const('Вы не заполнили количество ударов в следующих лунках:'),
            List(
                Format('+ {item}'),
                items='empty_holes'
            ),
            SwitchTo(
                Format(f'{GameKB.back_to_game[0]}'),
                id=GameKB.back_to_game[1],
                state=all_states.game.start,
            ),
            state=all_states.game.empty_holes,
            getter=g_hole.get_empty_holes
        )

    @staticmethod
    def end_game_window():
        return Window(
            Format('''Поздравляю {dialog_data[user].first_name} {dialog_data[user].last_name}! 
    Вы завершили турнир набрав {dialog_data[total_score].total} очков.
    '''),
            Button(
                Format(f'{MainKB.main_menu[0]}'),
                id=MainKB.main_menu[1],
                on_click=main_menu.on_main_menu,
            ),
            state=all_states.game.end,
        )
    # endregion


