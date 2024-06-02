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
            id="s_scroll_tournaments",
            item_id_getter=operator.attrgetter('id'),
            items="tournaments",
            on_click=on_click,
        ),
        id="tournament_ids",
        width=width, height=height,
    )


def paginated_impacts(
        on_click,
        width: int = SCROLLING_HEIGHT,
        height: int = SCROLLING_WIDTH
):
    return ScrollingGroup(
        Select(
            Format("{item[1]}"),
            id="s_scroll_impacts",
            item_id_getter=operator.itemgetter(0),
            items="impacts_list",
            on_click=on_click,
        ),
        id="impacts_kb",
        width=width, height=height,
    )


def paginated_holes(
        on_click,
        width: int = SCROLLING_HEIGHT,
        height: int = SCROLLING_WIDTH,
):
    return ScrollingGroup(
        Select(
            Format("{item[3]} №{item[1]} - ({item[2]})"),
            id="s_scroll_holes",
            item_id_getter=operator.itemgetter(0),
            items="holes_list",
            on_click=on_click,
        ),
        id="hole_ids_kb",
        width=width, height=height,
    )


def paginated_alphabet(
        on_click,
        width: int = SCROLLING_HEIGHT,
        height: int = SCROLLING_WIDTH
):
    return ScrollingGroup(
        Select(
            Format("{item[1]}"),
            id="s_scroll_letters",
            item_id_getter=operator.itemgetter(0),
            items="alphabet",
            on_click=on_click,
        ),
        id="alphabet_kb",
        width=width, height=height,
    )


def paginated_users(
        on_click,
        width: int = SCROLLING_HEIGHT,
        height: int = SCROLLING_WIDTH
):
    return ScrollingGroup(
        Select(
            Format("{pos}. {item.first_name} {item.last_name} [{item.id_telegram}]"),
            id="s_scroll_users",
            item_id_getter=operator.attrgetter('id'),
            items="users",
            on_click=on_click,
        ),
        id="users_ids",
        width=width, height=height,
    )


def paginated_admins(
        on_click,
        width: int = SCROLLING_HEIGHT,
        height: int = SCROLLING_WIDTH
):
    return ScrollingGroup(
        Select(
            Format("{pos}. {item.login}"),
            id="s_scroll_admins",
            item_id_getter=operator.attrgetter('id'),
            items="admins",
            on_click=on_click,
        ),
        id="admins_ids",
        width=width, height=height,
    )


def paginated_courses(
        on_click,
        width: int = SCROLLING_HEIGHT,
        height: int = SCROLLING_WIDTH
):
    return ScrollingGroup(
        Select(
            Format("{pos}. {item[1]}"),
            id="s_scroll_courses",
            item_id_getter=operator.itemgetter(0),
            items="courses_list",
            on_click=on_click,
        ),
        id="courses_ids",
        width=width, height=height,
    )


def paginated_holes_for_admin(
        on_click,
        width: int = SCROLLING_HEIGHT,
        height: int = SCROLLING_WIDTH
):
    return ScrollingGroup(
        Select(
            Format("№{item.number} - {item.par} - {item.difficulty}"),
            id="s_scroll_holes",
            item_id_getter=operator.attrgetter('id'),
            items="holes",
            on_click=on_click,
        ),
        id="holes_ids",
        width=width, height=height,
    )
