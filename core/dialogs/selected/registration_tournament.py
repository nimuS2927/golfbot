from typing import Any

from aiogram.filters.state import StatesGroup, State
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import Dialog, DialogManager
from aiogram_dialog.widgets.kbd import Button

# from core.dialogs.main_menu import getters
from core.dialogs.states import all_states


async def on_registration_tournament(
        callback: CallbackQuery,
        button: Button,
        manager: DialogManager,
):
    await manager.start(state=all_states.registration_tournament.start)

