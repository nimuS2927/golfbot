from aiogram_dialog import DialogManager


async def get_alphabet(
        # dialog_manager: DialogManager,
        # **middleware_data
):
    alphabet_upper = [chr(i) for i in range(65, 91)]
    alphabet_lower = [chr(i) for i in range(97, 123)]
    alphabet = alphabet_upper + alphabet_lower
    alphabet_sort = []
    for i in range(26):
        alphabet_sort.append(alphabet[i])
        alphabet_sort.append(alphabet[i + 26])
    return {'alphabet': alphabet_sort, 'stars': ''}


