from aiogram import types, Router
from aiogram.filters.command import Command
from aiogram_dialog import DialogManager, StartMode

from core.dialogs.services import all_services
from core.dialogs.states import all_states

router = Router(name=__name__)


@router.message(Command("start"))
async def start(message: types.Message, dialog_manager: DialogManager):
    session = dialog_manager.middleware_data.get('session')
    user = await all_services.user.get_user_by_tg_id(session=session, tg_id=message.from_user.id)
    if user:
        await dialog_manager.start(
            all_states.main.start,
            mode=StartMode.RESET_STACK,
        )
    else:
        await dialog_manager.start(
            all_states.registration_bot.start,
            mode=StartMode.RESET_STACK,
        )


@router.message(Command("admin"))
async def start(message: types.Message, dialog_manager: DialogManager):
    session = dialog_manager.middleware_data.get('session')
    user = await all_services.user.get_user_by_tg_id(session=session, tg_id=message.from_user.id)
    if user:
        await dialog_manager.start(
            all_states.main.start,
            mode=StartMode.RESET_STACK,
        )
    else:
        await dialog_manager.start(
            all_states.admin.forbidden,
            mode=StartMode.RESET_STACK,
        )
