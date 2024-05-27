import operator

from aiogram_dialog.widgets.kbd import Select, ScrollingGroup
from aiogram_dialog.widgets.text import Format


SCROLLING_HEIGHT = 6
SCROLLING_WIDTH = 3


def paginated_tournaments(
        on_click,
        width: int = SCROLLING_HEIGHT,
        height: int = SCROLLING_WIDTH
):
    return ScrollingGroup(
        Select(
            Format("{pos}. {item.name}"),
            id="s_scroll_products",
            item_id_getter=operator.attrgetter('id'),
            items="tournaments",
            on_click=on_click,
        ),
        id="tournament_ids",
        width=width, height=height,
    )


def paginated_holes(
        on_click,
        width: int = SCROLLING_HEIGHT,
        height: int = SCROLLING_WIDTH
):
    return ScrollingGroup(
        Select(
            Format("{item[3]} №{item[1]} - ({item[2]})"),
            id="s_scroll_products",
            item_id_getter=operator.itemgetter(0),
            items="holes_list",
            on_click=on_click,
        ),
        id="hole_ids_kb",
        width=width, height=height,
    )
