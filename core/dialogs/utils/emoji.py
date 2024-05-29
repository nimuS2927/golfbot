from aiogram_dialog import DialogManager


EMOJI_DICT = {
            2: '🔷',
            1: '🟦',
            0: '🟨',
            -1: '🟧',
            -2: '🔶',
            -3: '💠',
        }


async def get_emoji(
        dialog_manager: DialogManager,
        **middleware_data
):
    emoji = {
            2: '🔷',
            1: '🟦',
            0: '🟨',
            5: '🟧',
            4: '🔶',
            3: '💠',
        }
    return {'emoji': emoji}


def for_holes(key: int) -> str:
    data = EMOJI_DICT
    if key < -3:
        return data[-3]
    elif key > 2:
        return data[2]
    return data[key]
