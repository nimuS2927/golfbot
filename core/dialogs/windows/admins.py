import operator

from aiogram_dialog import Window, Data, DialogManager, ShowMode, Dialog
from aiogram_dialog.widgets.kbd import Cancel, Back, Button, SwitchTo, Row, Select, Calendar
from aiogram_dialog.widgets.text import Const, Format, List
from aiogram_dialog.widgets.media import StaticMedia, DynamicMedia
from aiogram_dialog.widgets.input import TextInput

from core.config import c_project
from core.dialogs.utils.custom_calendar import calendar_config
from core.main.keyboards.buttons import AdminKB, MainKB
from core.dialogs import keyboards
from core.dialogs.selected import admin as s_admin
from core.dialogs.getters import g_admin, g_tournament
from core.dialogs.states import all_states
from core.dialogs.utils import alphabet
import locale
locale.setlocale(
    category=locale.LC_ALL,
    locale="Russian"  # Note: do not use "de_DE" as it doesn't work
)


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
            SwitchTo(
                Format(f'{AdminKB.tournaments[0]}'),
                id=AdminKB.tournaments[1],
                state=all_states.admin.show_tournaments
            ),
            SwitchTo(
                Format(f'{AdminKB.admins[0]}'),
                id=AdminKB.admins[1],
                state=all_states.admin.show_admins,
            ),
            Button(
                Format(f'{AdminKB.users[0]}'),
                id=AdminKB.users[1],
                on_click=s_admin.on_show_users
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
                SwitchTo(
                    (Format(f'{MainKB.back[0]}')),
                    id=MainKB.back[1],
                    state=all_states.admin.start
                ),
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
                SwitchTo(
                    (Format(f'{MainKB.back[0]}')),
                    id=MainKB.back[1],
                    state=all_states.admin.show_tournaments
                ),
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
Название: {tournament_name}
Тип турнира: {tournament_type}
Максимальное количество флайтов: {tournament_flights}
Название поля: {course_name}
Стартует: {start_day}
Заканчивается: {end_day}
HCP: {hcp}'''),
            Row(
                Button(
                    Format(f'{AdminKB.start_tournaments[0]}'),
                    id=AdminKB.start_tournaments[1],
                    on_click=s_admin.on_start_tournament
                ),
                Button(
                    Format(f'{AdminKB.top_tournament[0]}'),
                    id=AdminKB.top_tournament[1],
                    on_click=s_admin.on_top
                ),
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
                SwitchTo(
                    (Format(f'{MainKB.back[0]}')),
                    id=MainKB.back[1],
                    state=all_states.admin.show_tournaments
                ),
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
    def empty_top_window():
        return Window(
            Const('Топ пока пуст'),
            SwitchTo(
                Const(f'{MainKB.back[0]}'),
                id=MainKB.back[1],
                state=all_states.admin.info_tournament
            ),
            state=all_states.admin.empty_top,
        )

    @staticmethod
    def top_window():
        return Window(
            Format('Топ игроков турнира:'),
            List(
                Format('{pos}. {item[0]} {item[1]} Удары/Лунки - {item[2]}/{item[3]} шт. Счёт: {item[4]}'),
                items='totalscores_list'
            ),
            SwitchTo(
                Const(f'{MainKB.back[0]}'),
                id=MainKB.back[1],
                state=all_states.admin.info_tournament
            ),
            state=all_states.admin.top,
            getter=g_tournament.get_totalscores
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
                SwitchTo(
                    (Format(f'{MainKB.back[0]}')),
                    id=MainKB.back[1],
                    state=all_states.admin.info_tournament
                ),
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
            getter=g_admin.get_tournament_for_edit
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
            Const('Выберите дату начала турнира'),
            Calendar(
                id='calendar',
                on_click=s_admin.on_selected_start_date,
                config=calendar_config
            ),
            state=all_states.admin.entered_start,
        )

    @staticmethod
    def entered_end_window():
        return Window(
            Const('Выберите дату конца турнира'),
            Calendar(
                id='calendar',
                on_click=s_admin.on_selected_end_date,
                config=calendar_config
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
                SwitchTo(
                    (Format(f'{MainKB.back[0]}')),
                    id=MainKB.back[1],
                    state=all_states.admin.start
                ),
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
    def empty_user_window():
        return Window(
            Format('Пользователи не зарегистрированы'),
            Row(
                SwitchTo(
                    (Format(f'{MainKB.back[0]}')),
                    id=MainKB.back[1],
                    state=all_states.admin.start
                ),
                Button(
                    Format(f'{AdminKB.close_admin_panel[0]}'),
                    id=AdminKB.close_admin_panel[1],
                    on_click=s_admin.on_close_admin_panel
                ),
            ),
            state=all_states.admin.empty_users,
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
                SwitchTo(
                    (Format(f'{MainKB.back[0]}')),
                    id=MainKB.back[1],
                    state=all_states.admin.show_users
                ),
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
                SwitchTo(
                    (Format(f'{MainKB.back[0]}')),
                    id=MainKB.back[1],
                    state=all_states.admin.info_user
                ),
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
    @staticmethod
    def choice_admin_window():
        return Window(
            Format('Выбери нужного админа'),
            keyboards.paginated_admins(
                on_click=s_admin.on_choice_admin,
                width=1,
                height=5,
            ),
            SwitchTo(
                Const(f'{AdminKB.admin_registration[0]}'),
                id=AdminKB.admin_registration[1],
                state=all_states.admin.info_admin_registration,
            ),
            Row(
                SwitchTo(
                    (Format(f'{MainKB.back[0]}')),
                    id=MainKB.back[1],
                    state=all_states.admin.start
                ),
                Button(
                    Format(f'{AdminKB.close_admin_panel[0]}'),
                    id=AdminKB.close_admin_panel[1],
                    on_click=s_admin.on_close_admin_panel
                ),
            ),
            state=all_states.admin.show_admins,
            getter=g_admin.get_admins
        )

    @staticmethod
    def info_admin_window():
        return Window(
            Format('''Информация о выбранном админе. 
ТГ ID: {admin.login}'''),
            Row(
                SwitchTo(
                    Format(f'{AdminKB.delete_admin[0]}'),
                    id=AdminKB.delete_admin[1],
                    state=all_states.admin.delete_admin
                ),
            ),
            SwitchTo(
                Const(f'{AdminKB.main_admin_panel[0]}'),
                id=AdminKB.main_admin_panel[1],
                state=all_states.admin.start
            ),
            Row(
                SwitchTo(
                    (Format(f'{MainKB.back[0]}')),
                    id=MainKB.back[1],
                    state=all_states.admin.show_admins
                ),
                Button(
                    Format(f'{AdminKB.close_admin_panel[0]}'),
                    id=AdminKB.close_admin_panel[1],
                    on_click=s_admin.on_close_admin_panel
                ),
            ),
            state=all_states.admin.info_admins,
            getter=g_admin.get_admin
        )

    @staticmethod
    def delete_admin_window():
        return Window(
            Format('''Вы точно хотите удалить этого админа?'''),
            Button(
                Const(f'{AdminKB.confirm[0]}'),
                id=AdminKB.confirm[1],
                on_click=s_admin.on_confirm_delete_admin
            ),
            Row(
                SwitchTo(
                    (Format(f'{MainKB.back[0]}')),
                    id=MainKB.back[1],
                    state=all_states.admin.info_admins
                ),
                Button(
                    Format(f'{AdminKB.close_admin_panel[0]}'),
                    id=AdminKB.close_admin_panel[1],
                    on_click=s_admin.on_close_admin_panel
                ),
            ),
            state=all_states.admin.delete_admin,
        )

    @staticmethod
    def info_admin_registration_window():
        return Window(
            Format('''Регистрационная информация о  админе. 
ТГ ID (логин): {dialog_data[login]}
Пароль: {dialog_data[stars_1]}'''),
            SwitchTo(
                Const(f'{AdminKB.entered_login[0]}'),
                id=AdminKB.entered_login[1],
                state=all_states.admin.entered_admin_login
            ),
            SwitchTo(
                Const(f'{AdminKB.entered_password[0]}'),
                id=AdminKB.entered_password[1],
                state=all_states.admin.entered_admin_password_1
            ),
            Row(
                Button(
                    Format(f'{AdminKB.confirm_registration[0]}'),
                    id=AdminKB.confirm_registration[1],
                    on_click=s_admin.on_confirm_registration_admin
                ),
                SwitchTo(
                    Const(f'{AdminKB.main_admin_panel[0]}'),
                    id=AdminKB.main_admin_panel[1],
                    state=all_states.admin.start
                ),
            ),
            Row(
                SwitchTo(
                    (Format(f'{MainKB.back[0]}')),
                    id=MainKB.back[1],
                    state=all_states.admin.show_admins
                ),
                Button(
                    Format(f'{AdminKB.close_admin_panel[0]}'),
                    id=AdminKB.close_admin_panel[1],
                    on_click=s_admin.on_close_admin_panel
                ),
            ),
            state=all_states.admin.info_admin_registration,
            getter=g_admin.get_admin_registration
        )

    @staticmethod
    def entered_admin_login_window():
        return Window(
            Const('Введите логин для админа:'),
            TextInput(
                id='admin_login',
                on_success=s_admin.on_entered_admin_login
            ),
            state=all_states.admin.entered_admin_login,
        )

    @staticmethod
    def entered_admin_password_1_window():
        return Window(
            Const('Введите пароль для админа:'),
            TextInput(
                id='admin_password_1',
                on_success=s_admin.on_entered_admin_password_1
            ),
            state=all_states.admin.entered_admin_password_1,
        )

    @staticmethod
    def entered_admin_password_2_window():
        return Window(
            Const('Продублируйте пароль для админа:'),
            TextInput(
                id='admin_password_2',
                on_success=s_admin.on_entered_admin_password_2
            ),
            state=all_states.admin.entered_admin_password_2,
        )
    # endregion Admins

    # region Courses
    @staticmethod
    def choice_course_window():
        return Window(
            Format('Выбери нужное поле'),
            keyboards.paginated_courses(
                on_click=s_admin.on_choice_course,
                width=1,
                height=5,
            ),
            SwitchTo(
                Const(f'{AdminKB.create_course[0]}'),
                id=AdminKB.create_course[1],
                state=all_states.admin.create_course
            ),
            Row(
                SwitchTo(
                    (Format(f'{MainKB.back[0]}')),
                    id=MainKB.back[1],
                    state=all_states.admin.start
                ),
                Button(
                    Format(f'{AdminKB.close_admin_panel[0]}'),
                    id=AdminKB.close_admin_panel[1],
                    on_click=s_admin.on_close_admin_panel
                ),
            ),
            state=all_states.admin.show_courses,
            getter=g_admin.get_courses
        )

    @staticmethod
    def create_course_entered_name_window():
        return Window(
            Const('Введите название поля:'),
            TextInput(
                id='course_name',
                on_success=s_admin.on_entered_course_name_for_create
            ),
            state=all_states.admin.create_course,
        )

    @staticmethod
    def empty_course_window():
        return Window(
            Format('У вас нет созданных полей'),
            SwitchTo(
                Const(f'{AdminKB.create_course[0]}'),
                id=AdminKB.create_course[1],
                state=all_states.admin.create_course
            ),
            Row(
                SwitchTo(
                    (Format(f'{MainKB.back[0]}')),
                    id=MainKB.back[1],
                    state=all_states.admin.start
                ),
                Button(
                    Format(f'{AdminKB.close_admin_panel[0]}'),
                    id=AdminKB.close_admin_panel[1],
                    on_click=s_admin.on_close_admin_panel
                ),
            ),
            state=all_states.admin.empty_courses,
        )

    @staticmethod
    def info_course_window():
        return Window(
            Format('Поле: {dialog_data[course][name]}'),
            Const('Лунки:'),
            List(
                Format('№{item.number} - {item.par} [пар] - {item.difficulty} [сложность]'),
                items='holes'
            ),
            Row(
                SwitchTo(
                    Const(f'{AdminKB.edit_holes[0]}'),
                    id=AdminKB.edit_holes[1],
                    state=all_states.admin.show_holes,
                    on_click=s_admin.on_holes_actions
                ),
                Button(
                    Const(f'{AdminKB.create_hole[0]}'),
                    id=AdminKB.create_hole[1],
                    on_click=s_admin.on_holes_actions
                ),
                SwitchTo(
                    Const(f'{AdminKB.delete_holes[0]}'),
                    id=AdminKB.delete_holes[1],
                    state=all_states.admin.show_holes,
                    on_click=s_admin.on_holes_actions
                ),
            ),
            Row(
                SwitchTo(
                    (Format(f'{MainKB.back[0]}')),
                    id=MainKB.back[1],
                    state=all_states.admin.show_courses
                ),
                Button(
                    Format(f'{AdminKB.close_admin_panel[0]}'),
                    id=AdminKB.close_admin_panel[1],
                    on_click=s_admin.on_close_admin_panel
                ),
            ),
            state=all_states.admin.info_course,
            getter=g_admin.get_holes
        )

    @staticmethod
    def info_course_without_holes_window():
        return Window(
            Format('Поле: {dialog_data[course][name]}'),
            Const('Лунки не созданы'),
            Row(
                Button(
                    Const(f'{AdminKB.create_hole[0]}'),
                    id=AdminKB.create_hole[1],
                    on_click=s_admin.on_holes_actions
                ),
                SwitchTo(
                    Format(f'{AdminKB.delete_course[0]}'),
                    id=AdminKB.delete_course[1],
                    state=all_states.admin.delete_course
                ),
            ),

            Row(
                SwitchTo(
                    (Format(f'{MainKB.back[0]}')),
                    id=MainKB.back[1],
                    state=all_states.admin.show_courses
                ),
                Button(
                    Format(f'{AdminKB.close_admin_panel[0]}'),
                    id=AdminKB.close_admin_panel[1],
                    on_click=s_admin.on_close_admin_panel
                ),
            ),
            state=all_states.admin.info_course_without_holes,
        )

    @staticmethod
    def show_holes_window():
        return Window(
            Format('Выбери нужную лунку'),
            keyboards.paginated_holes_for_admin(
                on_click=s_admin.on_choice_hole,
                width=3,
                height=6,
            ),
            Row(
                SwitchTo(
                    (Format(f'{MainKB.back[0]}')),
                    id=MainKB.back[1],
                    state=all_states.admin.info_course
                ),
                Button(
                    Format(f'{AdminKB.close_admin_panel[0]}'),
                    id=AdminKB.close_admin_panel[1],
                    on_click=s_admin.on_close_admin_panel
                ),
            ),
            state=all_states.admin.show_holes,
            getter=g_admin.get_holes
        )

    @staticmethod
    def info_hole_window():
        return Window(
            Format('(№{dialog_data[number]}) - ({dialog_data[par]} [пар]) - ({dialog_data[difficulty]} [сложность])'),
            SwitchTo(
                Const(f'{AdminKB.number_hole[0]}'),
                id=AdminKB.number_hole[1],
                state=all_states.admin.entered_number
            ),
            SwitchTo(
                Const(f'{AdminKB.par_hole[0]}'),
                id=AdminKB.par_hole[1],
                state=all_states.admin.entered_par
            ),
            SwitchTo(
                Const(f'{AdminKB.difficulty_hole[0]}'),
                id=AdminKB.difficulty_hole[1],
                state=all_states.admin.entered_difficulty
            ),
            Button(
                Const(f'{AdminKB.confirm[0]}'),
                id=AdminKB.confirm[1],
                on_click=s_admin.on_confirm_hole
            ),
            Row(
                SwitchTo(
                    (Format(f'{MainKB.back[0]}')),
                    id=MainKB.back[1],
                    state=all_states.admin.show_courses
                ),
                Button(
                    Format(f'{AdminKB.close_admin_panel[0]}'),
                    id=AdminKB.close_admin_panel[1],
                    on_click=s_admin.on_close_admin_panel
                ),
            ),
            state=all_states.admin.info_hole,
        )

    @staticmethod
    def entered_number_window():
        return Window(
            Const('Введите номер лунки:'),
            TextInput(
                id='hole_number',
                on_success=s_admin.on_entered_number
            ),
            state=all_states.admin.entered_number,
        )

    @staticmethod
    def entered_par_window():
        return Window(
            Const('Введите пар лунки:'),
            TextInput(
                id='hole_par',
                on_success=s_admin.on_entered_par
            ),
            state=all_states.admin.entered_par,
        )

    @staticmethod
    def entered_difficulty_window():
        return Window(
            Const('Введите сложность лунки:'),
            TextInput(
                id='hole_par',
                on_success=s_admin.on_entered_difficulty
            ),
            state=all_states.admin.entered_difficulty,
        )

    @staticmethod
    def delete_hole_window():
        return Window(
            Format('''Вы точно хотите удалить эту лунку?'''),
            Button(
                Const(f'{AdminKB.confirm[0]}'),
                id=AdminKB.confirm[1],
                on_click=s_admin.on_confirm_hole
            ),
            Row(
                SwitchTo(
                    (Format(f'{MainKB.back[0]}')),
                    id=MainKB.back[1],
                    state=all_states.admin.info_hole
                ),
                Button(
                    Format(f'{AdminKB.close_admin_panel[0]}'),
                    id=AdminKB.close_admin_panel[1],
                    on_click=s_admin.on_close_admin_panel
                ),
            ),
            state=all_states.admin.delete_hole,
        )

    @staticmethod
    def delete_course_window():
        return Window(
            Format('''Вы точно хотите удалить это поле?'''),
            Button(
                Const(f'{AdminKB.confirm[0]}'),
                id=AdminKB.confirm[1],
                on_click=s_admin.on_confirm_delete_course
            ),
            Row(
                SwitchTo(
                    (Format(f'{MainKB.back[0]}')),
                    id=MainKB.back[1],
                    state=all_states.admin.info_course_without_holes
                ),
                Button(
                    Format(f'{AdminKB.close_admin_panel[0]}'),
                    id=AdminKB.close_admin_panel[1],
                    on_click=s_admin.on_close_admin_panel
                ),
            ),
            state=all_states.admin.delete_course,
        )
    # endregion Courses
