from aiogram.enums import ContentType
from aiogram_dialog import DialogManager
from aiogram_dialog.api.entities import MediaAttachment


class Emoji:
    smile = '😃'
    heart = '❤'
    star = '⭐'
    gift = '🎁'
    phone = '📱'
    cart = '🛒'
    warning = '⚠'


async def get_emoji(
        dialog_manager: DialogManager,
        **middleware_data
):
    return {
        'emoji': Emoji(),
    }


