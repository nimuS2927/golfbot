from datetime import datetime
import re
from typing import Any, List, Optional, Dict

from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button

from core.dialogs.schemas.admins import GetAdmin, AdminSchemas, CreateAdmin
from core.dialogs.schemas.courses import Course, CreateCourse
from core.dialogs.schemas.holes import CreateHole, Hole, UpdateHolePartial
from core.dialogs.schemas.tournaments import Tournament, UpdateTournamentPartial, CreateTournament, TournamentWithCourse
from core.dialogs.schemas.users import UpdateUserPartial
from core.dialogs.states import all_states
from core.dialogs.services import all_services

# region Common func admins
from core.dialogs.utils.getters_obj_from_list import get_obj_by_attribute, get_obj_by_key
from core.main.keyboards.buttons import AdminKB


async def on_choice_letter(
        callback: CallbackQuery,
        button: Button,
        manager: DialogManager,
        item_id: str,
):
    item_id = int(item_id)
    # region Получаем промежуточные данные и входные переменные
    middleware_data = manager.middleware_data
    session = middleware_data.get('session')
    context = manager.current_context()
    alphabet = context.dialog_data.get('alphabet')
    # endregion
    # region Получаем введенные ранее символы пароля и дополняем его
    password = context.dialog_data.get('password')
    if not password:
        password = alphabet[item_id][1]
    else:
        password += alphabet[item_id][1]
    stars = '*' * len(password)
    # endregion

    # region Обновляем данные
    context.dialog_data.update(
        password=password,
        stars=stars,
    )
    # endregion
    await manager.switch_to(all_states.admin.authorization)


async def on_backspace_password(
        callback: CallbackQuery,
        button: Button,
        manager: DialogManager,
):
    # region Получаем промежуточные данные и входные переменные
    context = manager.current_context()
    password = context.dialog_data.get('password')
    if not password:
        return
    password = password[:-1]
    stars = '*' * len(password)
    # endregion
    # region Обновляем данные
    context.dialog_data.update(
        password=password,
        stars=stars,
    )
    # endregion
    await manager.switch_to(all_states.admin.authorization)


async def on_confirm_password(
        callback: CallbackQuery,
        button: Button,
        manager: DialogManager,
):
    # region Получаем промежуточные данные и входные переменные
    middleware_data = manager.middleware_data
    session = middleware_data.get('session')
    user_tg_id = callback.from_user.id
    context = manager.current_context()
    password = context.dialog_data.get('password')
    # endregion
    # region Проверяем введенный пароль
    if not password:
        await callback.message.answer('Вы не ввели пароль.')
        return
    # endregion
    # region Получаем админа по паролю и логину
    admin_form: GetAdmin = GetAdmin(
        login=str(user_tg_id),
        password=password,
    )
    admin_status: bool = await all_services.admin.get_admin_by_login(
        session=session,
        admin_form=admin_form,
    )
    # endregion
    if not admin_status:
        await manager.switch_to(state=all_states.admin.forbidden)  # В доступе отказано
    else:
        await manager.switch_to(state=all_states.admin.start)  # Авторизация пройдена


async def on_close_admin_panel(
        callback: CallbackQuery,
        button: Button,
        manager: DialogManager,
):
    await manager.done()


# endregion Common func admins


# region Tournaments
async def on_nearest_tournaments(
        callback: CallbackQuery,
        button: Button,
        manager: DialogManager,
):
    context = manager.current_context()
    kind_of = button.widget_id
    context.dialog_data.update(kind_of=kind_of)
    await manager.switch_to(state=all_states.admin.choice_tournament)


async def on_all_tournaments(
        callback: CallbackQuery,
        button: Button,
        manager: DialogManager,
):
    context = manager.current_context()
    kind_of = button.widget_id
    context.dialog_data.update(kind_of=kind_of)
    await manager.switch_to(state=all_states.admin.choice_tournament)


async def on_choice_tournament(
        callback: CallbackQuery,
        button: Button,
        manager: DialogManager,
        item_id: int,
):
    middleware_data = manager.middleware_data
    session = middleware_data.get('session')
    context = manager.current_context()
    tournament = await all_services.tournament.get_tournament_by_id(
        session=session,
        tournament_id=int(item_id),
        course_status=True
    )
    context.dialog_data.update(
        tournament_id=int(item_id),
        tournament=tournament,
        update_status=True,
    )
    await manager.switch_to(state=all_states.admin.info_tournament)


async def on_start_tournament(
        callback: CallbackQuery,
        button: Button,
        manager: DialogManager,
):
    # region Получаем промежуточные данные и входные переменные
    middleware_data = manager.middleware_data
    session = middleware_data.get('session')
    context = manager.current_context()
    tournament_id = context.dialog_data.get('tournament_id')
    tournament_dict = context.dialog_data.get('tournament')
    tournament: TournamentWithCourse = TournamentWithCourse.model_validate(tournament_dict)
    # endregion
    if tournament.status is False:
        tournament = await all_services.tournament.distributed_users_in_tournament(
            session=session,
            tournament_id=tournament_id
        )
        if tournament:
            manager.dialog_data.update(update_status=True)
            await callback.message.answer('Турнир запущен!!!')
            await manager.switch_to(state=all_states.admin.info_tournament)
    else:
        await callback.message.answer('Этот турнир уже запущен!')
        await manager.switch_to(state=all_states.admin.info_tournament)


async def on_top(
        callback: CallbackQuery,
        button: Button,
        manager: DialogManager,
):
    # region Получаем промежуточные и входные данные
    # region Сессия
    middleware_data = manager.middleware_data
    session = middleware_data.get('session')
    # endregion
    # region Данные из контекста
    context = manager.current_context()
    tournament_id: int = context.dialog_data.get('tournament_id')
    # endregion
    # endregion
    # region Получаем турнир с общими счетами каждого игрока
    tournament_dict = await all_services.tournament.get_tournament_for_top(
        session=session,
        tournament_id=int(tournament_id)
    )
    totalscores = tournament_dict.get('totalscores')
    # endregion
    if not totalscores:
        await manager.switch_to(all_states.admin.empty_top)
    else:
        context.dialog_data.update(totalscores=totalscores, tournament_type=tournament_dict['type'])
        await manager.switch_to(all_states.admin.top)


# region Ввод данных по турниру
async def on_entered_name(
        m: Message,
        widget: Any,
        manager: DialogManager,
        tournament_name: str,
):
    context = manager.current_context()
    valid_name = re.sub(r'[^\w\s]', '', tournament_name)
    if len(tournament_name) != len(valid_name):
        await m.reply('Название должно содержать только буквы и цифры')
        return
    context.dialog_data.update(tournament_name=tournament_name)
    await manager.switch_to(state=all_states.admin.edit_tournament)


async def on_entered_type(
        callback: CallbackQuery,
        button: Button,
        manager: DialogManager,
        item_id: str
):
    context = manager.current_context()
    types = context.dialog_data.get('types')
    context.dialog_data.update(tournament_type=types[int(item_id)][0])
    await manager.switch_to(state=all_states.admin.edit_tournament)


async def on_entered_flights(
        m: Message,
        widget: Any,
        manager: DialogManager,
        tournament_flights: str,
):
    context = manager.current_context()
    if not tournament_flights.isdigit():
        await m.reply('Количество флайтов должно содержать только цифры')
        return
    context.dialog_data.update(tournament_flights=tournament_flights)
    await manager.switch_to(state=all_states.admin.edit_tournament)


async def on_entered_course_name(
        callback: CallbackQuery,
        button: Button,
        manager: DialogManager,
        item_id: str
):
    context = manager.current_context()
    course_names = context.dialog_data.get('course_names')
    context.dialog_data.update(
        course_name=course_names[int(item_id)][0],
        id_course=course_names[int(item_id)][1]
    )
    await manager.switch_to(state=all_states.admin.edit_tournament)


async def on_entered_start(
        m: Message,
        widget: Any,
        manager: DialogManager,
        start_day: str,
):
    context = manager.current_context()
    if not (
            re.fullmatch(r'^20[23][0-9]-[01][0-9]-[0-3][0-9] [0-2][0-9]:[0-6][0-9]$', start_day.strip()) or
            re.fullmatch(r'^20[23][0-9]-[01][0-9]-[0-3][0-9]$', start_day.strip()) or
            re.fullmatch(r'^20[23][0-9]-[01][0-9]-[0-3][0-9] [0-2][0-9]:[0-6][0-9]:[0-6][0-9]$', start_day.strip())
    ):
        await m.reply('Дата не соответствует заданному формату')
        return
    try:
        if re.fullmatch(r'^20[23][0-9]-[01][0-9]-[0-3][0-9]$', start_day.strip()):
            start_day += ' 00:00:00'
        elif re.fullmatch(r'^20[23][0-9]-[01][0-9]-[0-3][0-9] [0-2][0-9]:[0-6][0-9]$', start_day.strip()):
            start_day += ':00'
        input_date = datetime.strptime(start_day.strip(), '%Y-%m-%d %H:%M:%S')
        end_day = context.dialog_data.get('end_day')
        if end_day.strip():
            if not isinstance(end_day, datetime):
                try:
                    end_day = datetime.strptime(end_day, '%Y-%m-%d %H:%M:%S')
                except ValueError:
                    end_day = datetime.strptime(end_day, '%Y-%m-%dT%H:%M:%S')
            if end_day < input_date:
                await m.reply(f'Дата начала турнира {input_date.strftime("%Y-%m-%d %H:%M:%S")!r}'
                              f' не может быть больше даты конца турнира {end_day.strftime("%Y-%m-%d %H:%M:%S")!r}')
                return
    except ValueError:
        await m.reply(f'Такой даты {start_day.strip()!r} не существует')
        return
    today = datetime.today()
    if today > input_date:
        await m.reply(
            f'Дата старта турнира {start_day.strip()!r} не может быть раньше сегодняшнего дня {today.strftime("%Y-%m-%d %H:%M:%S")!r}')
        return
    datetime_str = input_date.strftime('%Y-%m-%d %H:%M:%S')
    context.dialog_data.update(start_day=datetime_str)
    await manager.switch_to(state=all_states.admin.edit_tournament)


async def on_entered_end(
        m: Message,
        widget: Any,
        manager: DialogManager,
        end_day: str,
):
    context = manager.current_context()
    if not (
            re.fullmatch(r'^20[23][0-9]-[01][0-9]-[0-3][0-9] [0-2][0-9]:[0-6][0-9]$', end_day.strip()) or
            re.fullmatch(r'^20[23][0-9]-[01][0-9]-[0-3][0-9]$', end_day.strip()) or
            re.fullmatch(r'^20[23][0-9]-[01][0-9]-[0-3][0-9] [0-2][0-9]:[0-6][0-9]:[0-6][0-9]$', end_day.strip())
    ):
        await m.reply('Дата не соответствует заданному формату')
        return
    try:
        if re.fullmatch(r'^20[23][0-9]-[01][0-9]-[0-3][0-9]$', end_day.strip()):
            end_day += ' 23:59:59'
        elif re.fullmatch(r'^20[23][0-9]-[01][0-9]-[0-3][0-9] [0-2][0-9]:[0-6][0-9]$', end_day.strip()):
            end_day += ':59'
        input_date = datetime.strptime(end_day.strip(), '%Y-%m-%d %H:%M:%S')
        start_day = context.dialog_data.get('start_day')
        if start_day.strip():
            if not isinstance(start_day, datetime):
                try:
                    start_day = datetime.strptime(start_day, '%Y-%m-%d %H:%M:%S')
                except ValueError:
                    start_day = datetime.strptime(start_day, '%Y-%m-%dT%H:%M:%S')
            if start_day > input_date:
                await m.reply(f'Дата конца турнира {input_date.strftime("%Y-%m-%d %H:%M:%S")!r}'
                              f' не может быть меньше даты начала турнира {start_day.strftime("%Y-%m-%d %H:%M:%S")!r}')
                return
    except ValueError:
        await m.reply(f'Такой даты {end_day.strip()!r} не существует')
        return
    today = datetime.today()
    if today > input_date:
        await m.reply(
            f'Дата старта турнира {end_day.strip()!r} не может быть раньше сегодняшнего дня {today.strftime("%Y-%m-%d %H:%M:%S")!r}')
        return
    datetime_str = input_date.strftime('%Y-%m-%d %H:%M:%S')
    context.dialog_data.update(end_day=datetime_str)
    await manager.switch_to(state=all_states.admin.edit_tournament)


async def on_entered_hcp(
        m: Message,
        widget: Any,
        manager: DialogManager,
        hcp: str,
):
    context = manager.current_context()
    if not hcp.isdigit():
        await m.reply('HCP для турнира должно содержать только цифры')
        return
    if 0 > int(hcp) > 100:
        await m.reply('HCP это число от 0 до 100')
        return
    context.dialog_data.update(hcp=int(hcp))
    await manager.switch_to(state=all_states.admin.edit_tournament)


# endregion Ввод данных по турниру


# region create, update and delete tournaments
async def on_create_tournaments(
        callback: CallbackQuery,
        button: Button,
        manager: DialogManager,
):
    context = manager.current_context()
    action = button.widget_id
    context.dialog_data.update(action=action)
    await manager.switch_to(state=all_states.admin.edit_tournament)


async def on_update_tournaments(
        callback: CallbackQuery,
        button: Button,
        manager: DialogManager,
):
    context = manager.current_context()
    action = button.widget_id
    context.dialog_data.update(action=action, update_status=True)
    await manager.switch_to(state=all_states.admin.edit_tournament)


async def on_delete_tournaments(
        callback: CallbackQuery,
        button: Button,
        manager: DialogManager,
):
    context = manager.current_context()
    action = button.widget_id
    context.dialog_data.update(action=action, update_status=True)
    await manager.switch_to(state=all_states.admin.delete_tournament)


async def on_confirm_tournaments(
        callback: CallbackQuery,
        button: Button,
        manager: DialogManager,
):
    middleware_data = manager.middleware_data
    session = middleware_data.get('session')
    context = manager.current_context()
    dialog_data = context.dialog_data
    action = dialog_data.get('action')
    tournament_id = context.dialog_data.get('tournament_id')
    tournament_name = dialog_data.get('tournament_name')
    tournament_type = dialog_data.get('tournament_type')
    tournament_flights = dialog_data.get('tournament_flights')
    course_name = dialog_data.get('course_name')
    id_course = dialog_data.get('id_course')
    start_day = dialog_data.get('start_day')
    end_day = dialog_data.get('end_day')
    hcp = dialog_data.get('hcp')
    if action == AdminKB.create_tournaments[1]:
        try:
            create_tournaments: CreateTournament = CreateTournament(
                name=tournament_name,
                type=tournament_type,
                max_flights=tournament_flights,
                id_course=id_course,
                start=start_day,
                end=end_day,
                hcp=hcp if hcp else None,
            )
        except ValueError:
            await callback.message.answer('Вы заполнили не все требуемые поля')
            return
        tournament = await all_services.tournament.create_tournament(
            session=session,
            data=create_tournaments
        )
        context.dialog_data.update(
            update_status=True,
            tournament_id=tournament.id
        )
        await manager.switch_to(state=all_states.admin.info_tournament)
    elif action == AdminKB.update_tournaments[1]:
        update_data: UpdateTournamentPartial = UpdateTournamentPartial(
            name=tournament_name,
            type=tournament_type,
            max_flights=tournament_flights,
            id_course=id_course,
            start=start_day,
            end=end_day,
            hcp=hcp,
        )
        await all_services.tournament.partial_update_tournament(
            session=session,
            tournament_id=tournament_id,
            data=update_data,
        )
        context.dialog_data.update(update_status=True)
        await manager.switch_to(state=all_states.admin.info_tournament)
    elif action == AdminKB.delete_tournaments[1]:
        await all_services.tournament.delete_tournament(
            session=session,
            tournament_id=tournament_id,
        )
        await manager.switch_to(state=all_states.admin.show_tournaments)


# endregion Tournaments
# endregion Tournaments

# region Admins
async def on_choice_admin(
        callback: CallbackQuery,
        button: Button,
        manager: DialogManager,
        item_id: int,
):
    context = manager.current_context()
    context.dialog_data.update(admin_id=int(item_id))
    await manager.switch_to(state=all_states.admin.info_admins)


async def on_entered_admin_login(
        m: Message,
        widget: Any,
        manager: DialogManager,
        login: str,
):
    context = manager.current_context()
    try:
        int(login)
    except ValueError:
        await m.reply('Логин это ID телеграмма и он должен содержать только цифры')
        return
    context.dialog_data.update(login=login)
    await manager.switch_to(state=all_states.admin.info_admin_registration)


async def on_entered_admin_password_1(
        m: Message,
        widget: Any,
        manager: DialogManager,
        password_1: str,
):
    context = manager.current_context()
    valid_name = re.sub(r'[^a-zA-Z]', '', password_1)
    if len(password_1) != len(valid_name):
        await m.delete()
        await m.answer('Пароль должен содержать только заглавные и прописные буквы английского алфавита')
        return
    context.dialog_data.update(password_1=password_1, stars_1='*' * len(password_1))
    await m.delete()
    await manager.switch_to(state=all_states.admin.entered_admin_password_2)


async def on_entered_admin_password_2(
        m: Message,
        widget: Any,
        manager: DialogManager,
        password_2: str,
):
    context = manager.current_context()
    valid_name = re.sub(r'[^a-zA-Z]', '', password_2)
    if len(password_2) != len(valid_name):
        await m.delete()
        await m.answer('Пароль должен содержать только заглавные и прописные буквы английского алфавита')
        return
    password_1 = context.dialog_data.get('password_1')
    if password_1 != password_2:
        await m.delete()
        await m.answer('Введенные пароли не совпадают, повторите попытку')
        await manager.switch_to(state=all_states.admin.entered_admin_password_1)
        return
    context.dialog_data.update(password_2=password_2, stars_2='*' * len(password_2))
    await m.delete()
    await manager.switch_to(state=all_states.admin.info_admin_registration)


async def on_confirm_registration_admin(
        callback: CallbackQuery,
        button: Button,
        manager: DialogManager,
):
    middleware_data = manager.middleware_data
    session = middleware_data.get('session')
    context = manager.current_context()
    login = context.dialog_data.get('login')
    if not login:
        await callback.message.reply('Не введен логин')
        return
    password_1 = context.dialog_data.get('password_1')
    if not password_1:
        await callback.message.reply('Не введен пароль')
        return
    password_2 = context.dialog_data.get('password_2')
    if not password_2:
        await callback.message.reply('Не введен пароль второй раз')
        return
    admin_form: CreateAdmin = CreateAdmin(login=login, password=password_1)
    await all_services.admin.post_create_admin(
        session=session,
        admin_form=admin_form
    )
    await manager.switch_to(all_states.admin.show_admins)


async def on_confirm_delete_admin(
        callback: CallbackQuery,
        button: Button,
        manager: DialogManager,
):
    middleware_data = manager.middleware_data
    session = middleware_data.get('session')
    context = manager.current_context()
    dialog_data = context.dialog_data
    admin_id = dialog_data.get('admin_id')
    await all_services.admin.delete_admin_by_id(
        session=session,
        admin_id=admin_id,
    )
    await manager.switch_to(all_states.admin.show_admins)


# endregion Admins


# region Users
async def on_show_users(
        callback: CallbackQuery,
        button: Button,
        manager: DialogManager,
):
    context = manager.current_context()
    middleware_data = manager.middleware_data
    session = middleware_data.get('session')
    users = await all_services.user.get_users_all(
        session=session,
    )
    if not users:
        await manager.switch_to(state=all_states.admin.empty_users)
    else:
        await manager.switch_to(state=all_states.admin.show_users)


async def on_choice_user(
        callback: CallbackQuery,
        button: Button,
        manager: DialogManager,
        item_id: int,
):
    context = manager.current_context()
    context.dialog_data.update(user_id=int(item_id))
    await manager.switch_to(state=all_states.admin.info_user)


async def on_entered_handicap(
        m: Message,
        widget: Any,
        manager: DialogManager,
        handicap: str,
):
    context = manager.current_context()
    middleware_data = manager.middleware_data
    session = middleware_data.get('session')
    try:
        handicap = float(handicap)
        if -7 > handicap or handicap > 54:
            await m.reply('Введенное число выходит за пределы допустимого лимита. Гандикап должен быть от -7 до 54')
            return
    except ValueError:
        await m.reply('Гандикап должен иметь формат дробного числа разделенного точкой от -7 до 54')
        return
    user_id = context.dialog_data.get('user_id')
    update_data: UpdateUserPartial = UpdateUserPartial(handicap=handicap)
    user = await all_services.user.partial_update_user(
        session=session,
        data=update_data,
        user_id=user_id
    )
    context.dialog_data.update(user=user)
    await manager.switch_to(all_states.admin.info_user)


async def on_confirm_delete_user(
        callback: CallbackQuery,
        button: Button,
        manager: DialogManager,
):
    middleware_data = manager.middleware_data
    session = middleware_data.get('session')
    context = manager.current_context()
    dialog_data = context.dialog_data
    user_id = dialog_data.get('user_id')
    await all_services.user.delete_user(
        session=session,
        user_id=user_id
    )
    await manager.switch_to(all_states.admin.show_users)


# endregion Users


# region Courses
async def on_course(
        callback: CallbackQuery,
        button: Button,
        manager: DialogManager,
):
    # region получаем промежуточные данные
    middleware_data = manager.middleware_data
    session = middleware_data.get('session')
    context = manager.current_context()
    # endregion
    # region Получаем поля с лунками из БД
    courses = await all_services.course.get_courses_with_holes(
        session=session,
    )
    if not courses:
        await manager.switch_to(all_states.admin.empty_courses)
    else:
        context.dialog_data.update(
            courses=courses,
        )
        await manager.switch_to(all_states.admin.show_courses)
    # endregion


async def on_choice_course(
        callback: CallbackQuery,
        button: Button,
        manager: DialogManager,
        item_id: int,
):
    context = manager.current_context()
    middleware_data = manager.middleware_data
    session = middleware_data.get('session')
    courses = context.dialog_data.get('courses')
    courses_update = context.dialog_data.get('courses_update')
    if courses_update:
        courses = await all_services.course.get_courses_with_holes(
            session=session,
        )
        courses_update = False
        context.dialog_data.update(
            courses=courses,
            courses_update=courses_update,
        )
    middleware_data = manager.middleware_data
    session = middleware_data.get('session')
    course = get_obj_by_key(courses, 'id', int(item_id))
    # course = await all_services.course.get_course_by_id_with_holes(
    #     session=session,
    #     course_id=int(item_id)
    # )
    if not course.get('holes'):
        context.dialog_data.update(
            course=course,
            id_course=int(item_id)
        )
        await manager.switch_to(state=all_states.admin.info_course_without_holes)
    else:
        holes_dict: List[Dict[str, Any]] = sorted(course['holes'], key=lambda x: x['number'])
        holes: List[Hole] = [Hole.model_validate(hole) for hole in holes_dict]
        context.dialog_data.update(
            holes=holes,
            course=course,
            id_course=int(item_id)
        )
        await manager.switch_to(state=all_states.admin.info_course)


async def on_holes_actions(
        callback: CallbackQuery,
        button: Button,
        manager: DialogManager,
):
    context = manager.current_context()
    hole_action = button.widget_id
    if hole_action == AdminKB.edit_holes[1]:
        pass
    elif hole_action == AdminKB.create_hole[1]:
        holes = context.dialog_data.get('holes')
        if not holes:
            holes = []
        if len(holes) < 18:
            number = ' '
            par = ' '
            difficulty = ' '
            context.dialog_data.update(
                number=number,
                par=par,
                difficulty=difficulty,
            )
            await manager.switch_to(state=all_states.admin.info_hole)
        else:
            await callback.message.answer('На поле максимум 18 лунок')
            return
    elif hole_action == AdminKB.delete_holes[1]:
        pass
    context.dialog_data.update(
        hole_action=hole_action,
    )


async def on_choice_hole(
        callback: CallbackQuery,
        button: Button,
        manager: DialogManager,
        item_id: int,
):
    # region получаем промежуточные данные
    middleware_data = manager.middleware_data
    session = middleware_data.get('session')
    context = manager.current_context()
    # endregion
    holes = context.dialog_data.get('holes')
    hole = get_obj_by_attribute(holes, 'id', int(item_id))
    hole_action = context.dialog_data.get('hole_action')
    if hole_action == AdminKB.delete_holes[1]:
        context.dialog_data.update(
            hole=hole,
        )
        await manager.switch_to(state=all_states.admin.delete_hole)
    else:
        number = hole.number
        par = hole.par
        difficulty = hole.difficulty
        context.dialog_data.update(
            hole=hole,
            number=number,
            par=par,
            difficulty=difficulty,
        )
        await manager.switch_to(state=all_states.admin.info_hole)


async def on_entered_number(
        m: Message,
        widget: Any,
        manager: DialogManager,
        number: str,
):
    context = manager.current_context()
    middleware_data = manager.middleware_data
    session = middleware_data.get('session')
    try:
        number = int(number)
        if 1 > number or number > 18:
            await m.reply('Введенное число выходит за пределы допустимого лимита. Номер лунки должен быть от 1 до 18')
            return
    except ValueError:
        await m.reply('Номер лунки должен содержать только цифры')
        return
    context.dialog_data.update(number=int(number))
    await manager.switch_to(all_states.admin.info_hole)


async def on_entered_par(
        m: Message,
        widget: Any,
        manager: DialogManager,
        par: str,
):
    context = manager.current_context()
    try:
        par = int(par)
        if 3 > par or par > 5:
            await m.reply('Введенное число выходит за пределы допустимого лимита. Пар лунки должен быть от 3 до 5')
            return
    except ValueError:
        await m.reply('Пар лунки должен содержать только цифры')
        return
    context.dialog_data.update(par=int(par))
    await manager.switch_to(all_states.admin.info_hole)


async def on_entered_difficulty(
        m: Message,
        widget: Any,
        manager: DialogManager,
        difficulty: str,
):
    context = manager.current_context()
    try:
        difficulty = int(difficulty)
        if 1 > difficulty or difficulty > 18:
            await m.reply('Введенное число выходит за пределы допустимого лимита.'
                          ' Сложность лунки должена быть от 1 до 18')
            return
    except ValueError:
        await m.reply('Сложность лунки должна содержать только цифры')
        return
    context.dialog_data.update(difficulty=int(difficulty))
    await manager.switch_to(all_states.admin.info_hole)


async def on_confirm_hole(
        callback: CallbackQuery,
        button: Button,
        manager: DialogManager,
):
    # region получаем промежуточные данные
    middleware_data = manager.middleware_data
    session = middleware_data.get('session')
    context = manager.current_context()
    course = context.dialog_data.get('course')
    # endregion
    hole_action = context.dialog_data.get('hole_action')
    if hole_action == AdminKB.edit_holes[1]:
        hole_dict = context.dialog_data.get('hole')
        hole: Hole = Hole.model_validate(hole_dict)

        number = context.dialog_data.get('number')
        par = context.dialog_data.get('par')
        difficulty = context.dialog_data.get('difficulty')
        update_hole: UpdateHolePartial = UpdateHolePartial(
            number=number,
            par=par,
            difficulty=difficulty,
            id_course=course['id']
        )
        await all_services.hole.partial_update_hole(
            session=session,
            hole_id=hole.id,
            data=update_hole.model_dump(exclude_none=True, exclude_unset=True)
        )
        await manager.switch_to(all_states.admin.show_holes)

    elif hole_action == AdminKB.create_hole[1]:
        number = context.dialog_data.get('number')
        par = context.dialog_data.get('par')
        difficulty = context.dialog_data.get('difficulty')
        if len(course['holes']) < 18:
            try:
                create_hole: CreateHole = CreateHole(
                    number=number,
                    par=par,
                    difficulty=difficulty,
                    id_course=course['id']
                )
            except ValueError:
                await callback.message.answer('Не все параметры заполнены')
                return
            await all_services.hole.create_hole(
                session=session,
                data=create_hole.model_dump(exclude_none=True, exclude_unset=True)
            )

            await manager.switch_to(all_states.admin.info_course)
        else:
            await callback.message.answer('На одном поле максимум 18 лунок!')
            return
    elif hole_action == AdminKB.delete_holes[1]:
        hole_dict = context.dialog_data.get('hole')
        await all_services.hole.delete_hole(
            session=session,
            hole_id=hole_dict.id
        )
        # course_dict = await all_services.course.get_course_by_id_with_holes(
        #     session=session,
        #     course_id=course['id']
        # )
        # holes_dict: List[Dict[str, Any]] = sorted(course_dict['holes'], key=lambda x: x['number'])
        # holes: List[Hole] = [Hole.model_validate(hole) for hole in holes_dict]
        # context.dialog_data.update(
        #     holes=holes,
        #     course=course_dict
        # )
        await manager.switch_to(all_states.admin.show_holes)


async def on_entered_course_name_for_create(
        m: Message,
        widget: Any,
        manager: DialogManager,
        course_name: str,
):
    context = manager.current_context()
    middleware_data = manager.middleware_data
    session = middleware_data.get('session')
    valid_name = re.sub(r'[^\w\s]', '', course_name)
    if len(course_name) != len(valid_name):
        await m.reply('Название должно содержать только буквы и цифры')
        return
    create_course: CreateCourse = CreateCourse(name=course_name)
    await all_services.course.create_course(
        session=session,
        data=create_course.model_dump()
    )
    context.dialog_data.update(courses_update=True)
    await manager.switch_to(state=all_states.admin.show_courses)


async def on_confirm_delete_course(
        callback: CallbackQuery,
        button: Button,
        manager: DialogManager,
):
    context = manager.current_context()
    middleware_data = manager.middleware_data
    session = middleware_data.get('session')
    id_course = context.dialog_data.get('id_course')
    await all_services.course.delete_course(
        session=session,
        course_id=id_course
    )
    context.dialog_data.update(courses_update=True)
    await manager.switch_to(state=all_states.admin.start)
# endregion Courses
