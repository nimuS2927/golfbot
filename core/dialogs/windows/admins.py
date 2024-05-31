import operator

from aiogram_dialog import Window, Data, DialogManager, ShowMode, Dialog
from aiogram_dialog.widgets.kbd import Cancel, Back, Button, SwitchTo, Row, Select
from aiogram_dialog.widgets.text import Const, Format, List
from aiogram_dialog.widgets.media import StaticMedia, DynamicMedia
from aiogram_dialog.widgets.input import TextInput

from core.config import c_project
from core.main.keyboards.buttons import AdminKB, MainKB
from core.dialogs import keyboards
from core.dialogs.selected import admin as s_admin
from core.dialogs.getters import g_admin
from core.dialogs.states import all_states
from core.dialogs.utils import alphabet


class AdminWindows:

    @staticmethod
    def authorization_window():
        return Window(
            Format('''Привет, {start_data[user].first_name}, давай авторизуемся.
Введи пароль: {dialog_data[stars]}'''),
            keyboards.paginated_alphabet(
                on_click=s_admin.on_choice_letter,
                width=6,
                height=9,
            ),
            Row(
                Button(
                    Format(f'{AdminKB.backspace[0]}'),
                    id=AdminKB.backspace[1],
                    on_click=s_admin.on_backspace_password
                ),
                Button(
                    Format(f'{AdminKB.login[0]}'),
                    id=AdminKB.login[1],
                    on_click=s_admin.on_confirm_password
                ),
            ),
            Button(
                Format(f'{AdminKB.close_admin_panel[0]}'),
                id=AdminKB.close_admin_panel[1],
                on_click=s_admin.on_close_admin_panel
            ),
            state=all_states.admin.authorization,
            getter=alphabet.get_alphabet
        )

    @staticmethod
    def forbidden_window():
        return Window(
            Const('Вам отказано в доступе'),
            state=all_states.admin.forbidden,
        )

    @staticmethod
    def admin_window():
        return Window(
            Const('Привет, чем займемся?'),
            Button(
                Format(f'{AdminKB.tournaments[0]}'),
                id=AdminKB.tournaments[1],
                on_click=s_admin.on_tournaments
            ),
            Button(
                Format(f'{AdminKB.admins[0]}'),
                id=AdminKB.admins[1],
                on_click=s_admin.on_admins
            ),
            Button(
                Format(f'{AdminKB.users[0]}'),
                id=AdminKB.users[1],
                on_click=s_admin.on_users
            ),
            Button(
                Format(f'{AdminKB.courses[0]}'),
                id=AdminKB.courses[1],
                on_click=s_admin.on_course
            ),
            Button(
                Format(f'{AdminKB.close_admin_panel[0]}'),
                id=AdminKB.close_admin_panel[1],
                on_click=s_admin.on_close_admin_panel
            ),
            state=all_states.admin.start,
            # getter=[getters.get_emoji, getters.g_images.get_main]
        )

    # region tournament
    @staticmethod
    def show_tournament_window():
        return Window(
            Const('Турниры'),
            Button(
                Format(f'{AdminKB.nearest_tournaments[0]}'),
                id=AdminKB.nearest_tournaments[1],
                on_click=s_admin.on_nearest_tournaments
            ),
            Button(
                Format(f'{AdminKB.all_tournaments[0]}'),
                id=AdminKB.all_tournaments[1],
                on_click=s_admin.on_all_tournaments
            ),
            Button(
                Format(f'{AdminKB.create_tournaments[0]}'),
                id=AdminKB.create_tournaments[1],
                on_click=s_admin.on_create_tournaments
            ),
            Row(
                Back(Format(f'{MainKB.back[0]}')),
                Button(
                    Format(f'{AdminKB.close_admin_panel[0]}'),
                    id=AdminKB.close_admin_panel[1],
                    on_click=s_admin.on_close_admin_panel
                ),
            ),
            state=all_states.admin.show_tournaments,
            # getter=[getters.get_emoji, getters.g_images.get_main]
        )

    @staticmethod
    def choice_tournament_window():
        return Window(
            Format('Выбери нужный турнир'),
            keyboards.paginated_tournaments(
                on_click=s_admin.on_choice_tournament,
                width=1,
                height=5,
            ),
            Row(
                Back(Format(f'{MainKB.back[0]}')),
                Button(
                    Format(f'{AdminKB.close_admin_panel[0]}'),
                    id=AdminKB.close_admin_panel[1],
                    on_click=s_admin.on_close_admin_panel
                ),
            ),
            state=all_states.admin.choice_tournament,
            getter=g_admin.get_tournaments
        )

    @staticmethod
    def info_tournament_window():
        return Window(
            Format('''Информация о выбранном турнире. 
Название: {tournament.name}
Тип турнира: {tournament.type}
Максимальное количество флайтов: {tournament.max_flights}
Название поля: {tournament.course.name}
Стартует: {tournament.start}
Заканчивается: {tournament.end}
HCP: {tournament.hcp}'''),
            Button(
                Format(f'{AdminKB.start_tournaments[0]}'),
                id=AdminKB.start_tournaments[1],
                on_click=s_admin.on_start_tournament
            ),
            Row(
                Button(
                    Format(f'{AdminKB.update_tournaments[0]}'),
                    id=AdminKB.update_tournaments[1],
                    on_click=s_admin.on_update_tournaments
                ),
                Button(
                    Format(f'{AdminKB.delete_tournaments[0]}'),
                    id=AdminKB.delete_tournaments[1],
                    on_click=s_admin.on_delete_tournaments
                ),
            ),
            SwitchTo(
                Const(f'{AdminKB.main_admin_panel[0]}'),
                id=AdminKB.main_admin_panel[1],
                state=all_states.admin.start
            ),
            Row(
                Back(Format(f'{MainKB.back[0]}')),
                Button(
                    Format(f'{AdminKB.close_admin_panel[0]}'),
                    id=AdminKB.close_admin_panel[1],
                    on_click=s_admin.on_close_admin_panel
                ),
            ),
            state=all_states.admin.info_tournament,
            getter=g_admin.get_tournament
        )

    @staticmethod
    def delete_tournament_window():
        return Window(
            Format('''Название: {tournament_name}
Тип турнира: {tournament_type}
Максимальное количество флайтов: {tournament_flights}
Название поля: {course_name}
Стартует: {start_day}
Заканчивается: {end_day}
HCP: {hcp}'''),
            Button(
                Const(f'{AdminKB.confirm[0]}'),
                id=AdminKB.confirm[1],
                on_click=s_admin.on_confirm_tournaments
            ),
            Row(
                Back(Format(f'{MainKB.back[0]}')),
                Button(
                    Format(f'{AdminKB.close_admin_panel[0]}'),
                    id=AdminKB.close_admin_panel[1],
                    on_click=s_admin.on_close_admin_panel
                ),
            ),
            state=all_states.admin.delete_tournament,
            getter=g_admin.get_tournament
        )

    @staticmethod
    def edit_tournament_window():
        return Window(
            Format('''Название: {tournament_name}
Тип турнира: {tournament_type}
Максимальное количество флайтов: {tournament_flights}
Название поля: {course_name}
Стартует: {start_day}
Заканчивается: {end_day}
HCP: {hcp}'''),
            SwitchTo(
                Format(f'{AdminKB.entered_name[0]}'),
                id=AdminKB.entered_name[1],
                state=all_states.admin.entered_name
            ),
            SwitchTo(
                Format(f'{AdminKB.entered_type[0]}'),
                id=AdminKB.entered_type[1],
                state=all_states.admin.entered_type
            ),
            SwitchTo(
                Format(f'{AdminKB.entered_flights[0]}'),
                id=AdminKB.entered_flights[1],
                state=all_states.admin.entered_flights
            ),
            SwitchTo(
                Format(f'{AdminKB.entered_course_name[0]}'),
                id=AdminKB.entered_course_name[1],
                state=all_states.admin.entered_course_name
            ),
            SwitchTo(
                Format(f'{AdminKB.entered_start[0]}'),
                id=AdminKB.entered_start[1],
                state=all_states.admin.entered_start
            ),
            SwitchTo(
                Format(f'{AdminKB.entered_end[0]}'),
                id=AdminKB.entered_end[1],
                state=all_states.admin.entered_end
            ),
            SwitchTo(
                Format(f'{AdminKB.entered_hcp[0]}'),
                id=AdminKB.entered_hcp[1],
                state=all_states.admin.entered_hcp
            ),
            Button(
                Const(f'{AdminKB.confirm[0]}'),
                id=AdminKB.confirm[1],
                on_click=s_admin.on_confirm_tournaments
            ),
            Row(
                SwitchTo(
                    Const(f'{AdminKB.main_admin_panel[0]}'),
                    id=AdminKB.main_admin_panel[1],
                    state=all_states.admin.start
                ),
                Button(
                    Format(f'{AdminKB.close_admin_panel[0]}'),
                    id=AdminKB.close_admin_panel[1],
                    on_click=s_admin.on_close_admin_panel
                ),
            ),
            state=all_states.admin.edit_tournament,
            getter=g_admin.get_tournament
        )

    @staticmethod
    def entered_name_window():
        return Window(
            Const('Введите название турнира:'),
            TextInput(
                id='tournament_name',
                on_success=s_admin.on_entered_name
            ),
            state=all_states.admin.entered_name,
        )

    @staticmethod
    def entered_type_window():
        return Window(
            Const('Выберите тип турнира:'),
            Select(
                Format('{item[0]}'),
                id='s_tournament_type',
                item_id_getter=operator.itemgetter(1),
                on_click=s_admin.on_entered_type,
                items="types"
            ),
            state=all_states.admin.entered_type,
            getter=g_admin.get_tournament_types
        )

    @staticmethod
    def entered_flights_window():
        return Window(
            Const('Введите максимальное количество флайтов:'),
            TextInput(
                id='tournament_flights',
                on_success=s_admin.on_entered_flights
            ),
            state=all_states.admin.entered_flights,
        )

    @staticmethod
    def entered_course_name_window():
        return Window(
            Const('Выберите поле:'),
            Select(
                Format('{item[0]}'),
                id='s_tournament_course_name',
                item_id_getter=operator.itemgetter(2),
                on_click=s_admin.on_entered_course_name,
                items="course_names"
            ),
            state=all_states.admin.entered_course_name,
            getter=g_admin.get_courses_name
        )

    @staticmethod
    def entered_start_window():
        return Window(
            Const('Введите дату начала турнира в формате YYYY-MM-DD HH:MM:SS '
                  '(часы, минуты и секунды опционально, если не указано автоматически будет 00:00:00 : '
                  '* время задается обязательно в формате HH:MM или HH:MM:SS : '),
            TextInput(
                id='start_day',
                on_success=s_admin.on_entered_start
            ),
            state=all_states.admin.entered_start,
        )

    @staticmethod
    def entered_end_window():
        return Window(
            Const('Введите дату конца турнира в формате YYYY-MM-DD HH:MM:SS '
                  '(часы и минуты опционально, если не указано автоматически будет 23:59:59'
                  '* время задается обязательно в формате HH:MM или HH:MM:SS : '),
            TextInput(
                id='end_day',
                on_success=s_admin.on_entered_end
            ),
            state=all_states.admin.entered_end,
        )

    @staticmethod
    def entered_hcp_window():
        return Window(
            Const('Введите HCP для турнира:'),
            TextInput(
                id='tournament_hcp',
                on_success=s_admin.on_entered_hcp
            ),
            state=all_states.admin.entered_hcp,
        )
    # endregion tournament

    # region Users
    @staticmethod
    def choice_user_window():
        return Window(
            Format('Выбери нужного пользователя'),
            keyboards.paginated_users(
                on_click=s_admin.on_choice_user,
                width=1,
                height=5,
            ),
            Row(
                Back(Format(f'{MainKB.back[0]}')),
                Button(
                    Format(f'{AdminKB.close_admin_panel[0]}'),
                    id=AdminKB.close_admin_panel[1],
                    on_click=s_admin.on_close_admin_panel
                ),
            ),
            state=all_states.admin.show_users,
            getter=g_admin.get_users
        )

    @staticmethod
    def info_user_window():
        return Window(
            Format('''Информация о выбранном пользователе. 
Имя: {user.first_name}
Фамилия: {user.last_name}
ID телеграмма: {user.id_telegram}
Телефон: {user.phone}
Гандикап: {user.handicap}'''),
            Row(
                SwitchTo(
                    Format(f'{AdminKB.update_handicap[0]}'),
                    id=AdminKB.update_handicap[1],
                    state=all_states.admin.entered_handicap
                ),
                SwitchTo(
                    Format(f'{AdminKB.delete_user[0]}'),
                    id=AdminKB.delete_user[1],
                    state=all_states.admin.delete_user
                ),
            ),
            SwitchTo(
                Const(f'{AdminKB.main_admin_panel[0]}'),
                id=AdminKB.main_admin_panel[1],
                state=all_states.admin.start
            ),
            Row(
                Back(Format(f'{MainKB.back[0]}')),
                Button(
                    Format(f'{AdminKB.close_admin_panel[0]}'),
                    id=AdminKB.close_admin_panel[1],
                    on_click=s_admin.on_close_admin_panel
                ),
            ),
            state=all_states.admin.info_user,
            getter=g_admin.get_user
        )

    @staticmethod
    def delete_user_window():
        return Window(
            Format('''Вы точно хотите удалить этого пользователя?'''),
            Button(
                Const(f'{AdminKB.confirm[0]}'),
                id=AdminKB.confirm[1],
                on_click=s_admin.on_confirm_delete_user
            ),
            Row(
                Back(Format(f'{MainKB.back[0]}')),
                Button(
                    Format(f'{AdminKB.close_admin_panel[0]}'),
                    id=AdminKB.close_admin_panel[1],
                    on_click=s_admin.on_close_admin_panel
                ),
            ),
            state=all_states.admin.delete_user,
        )

    @staticmethod
    def entered_handicap_window():
        return Window(
            Const('Введите гандикап:'),
            TextInput(
                id='handicap',
                on_success=s_admin.on_entered_handicap
            ),
            state=all_states.admin.entered_handicap,
        )
    # endregion Users

    # region Admins

    # endregion Admins

    # region Courses

    # endregion Courses

