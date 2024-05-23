from aiogram_dialog import DialogManager


async def get_registration_data(
        dialog_manager: DialogManager,
        **middleware_data):
    dialog_data = dialog_manager.current_context().dialog_data

    first_name = dialog_data.get('first_name')
    last_name = dialog_data.get('last_name')
    phone = dialog_data.get('phone')
    handicap = dialog_data.get('handicap')

    return {
        'first_name': first_name if first_name else '',
        'last_name': last_name if last_name else '',
        'phone': phone if phone else '',
        'handicap': handicap if handicap else '',
    }