from typing import Any

from aiogram.filters.state import StatesGroup, State
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import Dialog, DialogManager
from aiogram_dialog.widgets.kbd import Button

# from core.dialogs.main_menu import getters
from core.dialogs.schemas.users import CreateUser, User
from core.dialogs.services import all_services
from core.dialogs.states import all_states


async def on_registration_bot(
        callback: CallbackQuery,
        button: Button,
        manager: DialogManager,
):
    await manager.start(state=all_states.registration_bot.start)


async def on_entered_first_name(
        m: Message,
        widget: Any,
        manager: DialogManager,
        first_name: str,
):
    ctx = manager.current_context()
    if not first_name.isalpha():
        await m.reply('Фамилия должна содержать только буквенные символы')
        return
    ctx.dialog_data.update(first_name=first_name)
    await manager.switch_to(all_states.registration_bot.start)


async def on_entered_last_name(
        m: Message,
        widget: Any,
        manager: DialogManager,
        last_name: str,
):
    ctx = manager.current_context()
    if not last_name.isalpha():
        await m.reply('Имя должно содержать только буквенные символы')
        return
    ctx.dialog_data.update(last_name=last_name)
    await manager.switch_to(all_states.registration_bot.start)


async def on_entered_phone(
        m: Message,
        widget: Any,
        manager: DialogManager,
        phone: str,
):
    ctx = manager.current_context()
    if not phone.isdigit() or len(phone) != 11:
        await m.reply('Телефон должен быть в формате 8 ххх ххх хх хх (без пробелов)')
        return
    ctx.dialog_data.update(phone=phone)
    await manager.switch_to(all_states.registration_bot.start)


async def on_entered_handicap(
        m: Message,
        widget: Any,
        manager: DialogManager,
        handicap: str,
):
    ctx = manager.current_context()
    try:
        handicap = float(handicap)
        if -7 > handicap or handicap > 54:
            await m.reply('Введенное число выходит за пределы допустимого лимита. Гандикап должен быть от -7 до 54')
            return
    except ValueError:
        await m.reply('Гандикап должен иметь формат дробного числа разделенного точкой от -7 до 54')
        return

    ctx.dialog_data.update(handicap=handicap)
    await manager.switch_to(all_states.registration_bot.start)


async def on_entered_confirm(
        callback: CallbackQuery,
        button: Button,
        manager: DialogManager,
):
    ctx = manager.current_context()
    tg_id = callback.from_user.id
    first_name = ctx.dialog_data.get('first_name')
    last_name = ctx.dialog_data.get('last_name')
    phone = ctx.dialog_data.get('phone')
    handicap = ctx.dialog_data.get('handicap')
    create_user: CreateUser = CreateUser(
        id_telegram=tg_id,
        first_name=first_name,
        last_name=last_name,
        phone=phone,
        handicap=handicap,
    )
    middleware_data = manager.middleware_data
    session = middleware_data.get('session')
    user: User = await all_services.user.create_user(session=session, data=create_user.model_dump())
    await manager.switch_to(all_states.registration_bot.end)
