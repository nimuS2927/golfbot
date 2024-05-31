from datetime import datetime
import re
from typing import Any, List, Optional, Dict

from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button

from core.dialogs.schemas.admins import GetAdmin, AdminSchemas
from core.dialogs.schemas.tournaments import Tournament, UpdateTournamentPartial, CreateTournament, TournamentWithCourse
from core.dialogs.states import all_states
from core.dialogs.services import all_services

# region Common func admins
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
async def on_tournaments(
        callback: CallbackQuery,
        button: Button,
        manager: DialogManager,
):
    await manager.switch_to(state=all_states.admin.show_tournaments)


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
        tournament=tournament
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

        tournament = await all_services.tournament.get_tournament_by_id(
            session=session,
            tournament_id=tournament_id,
            course_status=True
        )
        if tournament.status:
            manager.dialog_data.update(tournament=tournament)
            await callback.message.answer('Турнир запущен!!!')
            await manager.switch_to(state=all_states.admin.info_tournament)
    else:
        await callback.message.answer('Этот турнир уже запущен!')
        await manager.switch_to(state=all_states.admin.info_tournament)


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
        await m.reply(f'Дата старта турнира {start_day.strip()!r} не может быть раньше сегодняшнего дня {today!r}')
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
        await m.reply(f'Дата старта турнира {end_day.strip()!r} не может быть раньше сегодняшнего дня {today!r}')
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
    context.dialog_data.update(action=action)
    await manager.switch_to(state=all_states.admin.edit_tournament)


async def on_delete_tournaments(
        callback: CallbackQuery,
        button: Button,
        manager: DialogManager,
):
    context = manager.current_context()
    action = button.widget_id
    context.dialog_data.update(action=action)
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
                hcp=hcp,
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
            tournament_id=tournament_id
        )
        await manager.switch_to(state=all_states.admin.choice_tournament)


# endregion Tournaments


# region Admins
async def on_admins(
        callback: CallbackQuery,
        button: Button,
        manager: DialogManager,
):
    await manager.switch_to(state=all_states.admin.show_admin)


# endregion Admins


# region Users
async def on_users(
        callback: CallbackQuery,
        button: Button,
        manager: DialogManager,
):
    pass


# endregion Users


# region Courses
async def on_course(
        callback: CallbackQuery,
        button: Button,
        manager: DialogManager,
):
    pass
# endregion Courses
