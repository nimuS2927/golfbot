from aiogram_dialog import DialogManager


async def get_alphabet(
        dialog_manager: DialogManager,
        **middleware_data
):
    alphabet_upper = [chr(i) for i in range(65, 91)]
    alphabet_lower = [chr(i) for i in range(97, 123)]
    alphabet = alphabet_upper + alphabet_lower
    alphabet_sort = []
    for i in range(26):
        alphabet_sort.append(alphabet[i])
        alphabet_sort.append(alphabet[i + 26])
    alphabet_sort = [(i, sym) for i, sym in enumerate(alphabet_sort)]
    stars = dialog_manager.current_context().dialog_data.get('stars')
    if not stars:
        stars = ' '
    dialog_manager.current_context().dialog_data.update(
        alphabet=alphabet_sort,
        stars=stars
    )
    return {'alphabet': alphabet_sort}

#
# alphabet_upper = [chr(i) for i in range(65, 91)]
# alphabet_lower = [chr(i) for i in range(97, 123)]
# print(alphabet_upper)
# print(alphabet_lower)
#
# alphabet = alphabet_upper + alphabet_lower
# alphabet_sort = []
# for i in range(26):
#     alphabet_sort.append(alphabet[i])
#     alphabet_sort.append(alphabet[i + 26])
# print(alphabet_sort)
# alphabet_sort = [(i, sym) for i, sym in enumerate(alphabet_sort)]
# print(alphabet_sort)

