from aiogram import types, Router
from aiogram.filters.command import Command
from aiogram_dialog import DialogManager, StartMode

from core.dialogs.states import all_states

router = Router(name=__name__)


@router.message(Command("start"))
async def start(message: types.Message, dialog_manager: DialogManager):
    await dialog_manager.start(
        all_states.main.start,
        mode=StartMode.RESET_STACK,
    )

