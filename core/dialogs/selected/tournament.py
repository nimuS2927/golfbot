from typing import Any, List

from aiogram.filters.state import StatesGroup, State
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import Dialog, DialogManager
from aiogram_dialog.widgets.kbd import Button

from core.dialogs.getters import g_user
from core.dialogs.schemas.tournaments import Tournament, CreateTournament
from core.dialogs.schemas.users import User
from core.dialogs.states import all_states
from core.dialogs.services import all_services


async def on_registration_tournament(
        callback: CallbackQuery,
        button: Button,
        manager: DialogManager,
):
    middleware_data = manager.middleware_data
    session = middleware_data.get('session')
    user_tg_id = callback.from_user.id
    try:
        user: User = await all_services.user.get_user_by_tg_id(session=session, tg_id=user_tg_id)
        objs: List[Tournament] = await all_services.tournament.get_tournament_nearest_without_users(
            session=session,
            user_tg_id=user_tg_id
        )
        if not objs:
            await manager.start(state=all_states.registration_tournament.empty)
        else:
            await manager.start(state=all_states.registration_tournament.start)
    except:
        await manager.start(state=all_states.registration_tournament.anonymous)


async def on_choice_tournament(
        callback: CallbackQuery,
        button: Button,
        manager: DialogManager,
        item_id: int,
):
    context = manager.current_context()
    context.dialog_data.update(tournament_id=item_id)
    await manager.switch_to(all_states.registration_tournament.info)


async def on_entered_confirm(
        callback: CallbackQuery,
        button: Button,
        manager: DialogManager,
):
    user_tg_id = callback.from_user.id

    ctx = manager.current_context()
    tournament_id = ctx.dialog_data.get('tournament_id')

    middleware_data = manager.middleware_data
    session = middleware_data.get('session')
    tournament: dict = await all_services.tournament.add_user_in_tournament(
        session=session,
        tournament_id=tournament_id,
        user_tg_id=user_tg_id,
    )
    await manager.switch_to(all_states.registration_tournament.end)
