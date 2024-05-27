from typing import Any, List, Optional, Dict

from aiogram.filters.state import StatesGroup, State
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import Dialog, DialogManager
from aiogram_dialog.widgets.kbd import Button

from core.dialogs.game_rules import stroke_play_nett, stableford
from core.dialogs.getters import g_user
from core.dialogs.schemas.holes import Hole
from core.dialogs.schemas.scores import CreateScore, Score
from core.dialogs.schemas.totalscores import TotalScore, CreateTotalScore, TotalForFirstCreate
from core.dialogs.schemas.tournaments import Tournament, CreateTournament
from core.dialogs.schemas.users import User
from core.dialogs.states import all_states
from core.dialogs.services import all_services


async def on_list_available_tournament(
        callback: CallbackQuery,
        button: Button,
        manager: DialogManager,
):
    middleware_data = manager.middleware_data
    session = middleware_data.get('session')
    user_tg_id = callback.from_user.id
    objs: List[Tournament] = await all_services.tournament.get_tournaments_for_game(
        session=session,
        user_tg_id=user_tg_id
    )
    if not objs:
        await manager.start(state=all_states.game.empty)
    else:
        await manager.start(state=all_states.game.choice)


async def on_choice_tournament(
        callback: CallbackQuery,
        button: Button,
        manager: DialogManager,
        item_id: int,
):
    context = manager.current_context()
    tg_id = callback.from_user.id
    session = manager.middleware_data.get('session')
    tournament: Tournament = await all_services.tournament.get_tournament_by_id(session=session, tournament_id=item_id)
    user: User = await all_services.user.get_user_by_tg_id(session=session, tg_id=tg_id)
    holes: List[Hole] = await all_services.hole.get_holes_by_course_id(
        session=session, course_id=tournament.id_course)
    scores_list: Optional[List[Score]] = context.dialog_data.get('scores')
    total_score: Optional[TotalScore] = context.dialog_data.get('total_score')
    if scores_list is None:
        scores_list = []
        # Создаем "Счет" для каждой лунки + "итоговый счет" для юзера

        create_total_score: TotalForFirstCreate = TotalForFirstCreate(
            id_tournament=item_id,
            id_user=user.id,
            total=0,
        )
        total_score: TotalScore = await all_services.totalscores.create_totalscore(
            session=session,
            data=create_total_score.model_dump()
        )
        for hole in holes:
            create_score: CreateScore = CreateScore(
                    id_tournament=item_id,
                    id_hole=hole.id,
                    id_user=user.id,
                    id_total_score=total_score.id,
            )
            score: Score = await all_services.score.create_score(session=session, data=create_score.model_dump())
            scores_list.append(score)

    context.dialog_data.update(
        tournament_id=item_id,
        tournament=tournament,
        user=user,
        scores=scores_list,
        total_score=total_score,
        holes=holes
    )
    await manager.switch_to(all_states.game.start)


async def on_choice_holes(
        callback: CallbackQuery,
        button: Button,
        manager: DialogManager,
        item_id: int,
):
    context = manager.current_context()
    session = manager.middleware_data.get('session')
    hole: Hole = await all_services.hole.get_hole_by_id(session=session, hole_id=item_id)
    context.dialog_data.update(hole_id=item_id, hole=hole)

    await manager.switch_to(all_states.game.result)


async def on_entered_impacts(
        m: Message,
        widget: Any,
        manager: DialogManager,
        impacts: str,
):
    if not impacts.isdigit():
        await m.reply('Количество ударов не может содержать буквы')
        return
    user_tg_id = m.from_user.id
    middleware_data = manager.middleware_data
    session = middleware_data.get('session')
    context = manager.current_context()
    tournament_id = context.dialog_data.get('tournament_id')
    scores_list: Optional[List[Score]] = context.dialog_data.get('scores')
    total_score: Optional[TotalScore] = context.dialog_data.get('total_score')
    tournament: Optional[Tournament] = context.dialog_data.get('tournament')
    user: Optional[User] = context.dialog_data.get('user')
    hole: Optional[Hole] = context.dialog_data.get('hole')
    holes_ids: Optional[Dict[int]] = context.dialog_data.get('holes_ids')
    if not holes_ids:
        holes_ids = {}

    for sc in scores_list:
        if sc.id_hole == hole.id:
            sc.impacts = int(impacts)
            holes_ids[hole.id] = [sc.impacts, hole.par, hole.difficulty]
    handicap = round(user.handicap)
    if tournament.type == 'stableford':
        total = 0
        for id_, v in holes_ids.items():
            points = stableford(
                impacts=v[0],
                par=v[1],
                index=v[2],
                handicap=handicap,
                hcp=tournament.hcp,
            )
            total += points
        total_score.total = total
        print('*' * 50)
        print('stableford')
        print(holes_ids)
        print(total_score.total)
        print('*' * 50)
    else:
        total = 0
        for sc in scores_list:
            try:
                total += sc.impacts
            except ValueError:
                continue
        if tournament.type == 'stroke play':
            total_score.total = total
            print('*' * 50)
            print('stroke play')
            print(total_score.total)
            print('*' * 50)
        elif tournament.type == 'stroke play nett':
            total_score.total = stroke_play_nett(total_impacts=total, handicap=handicap, hcp=tournament.hcp)
            print('*' * 50)
            print('stroke play nett')
            print(total_score.total)
            print('*' * 50)

    context.dialog_data.update(scores=scores_list, totalscore=total_score, holes_ids=holes_ids)

    await manager.switch_to(all_states.game.start)


async def on_completed_game(
        callback: CallbackQuery,
        button: Button,
        manager: DialogManager,
):
    context = manager.current_context()
    middleware_data = manager.middleware_data
    session = middleware_data.get('session')
    scores_list: Optional[List[Score]] = context.dialog_data.get('scores')
    empty_hole_numbers = []
    for sc in scores_list:
        if not sc.impacts:
            hole: Hole = await all_services.hole.get_hole_by_id(session=session, hole_id=sc.id_hole)
            empty_hole_numbers.append(hole.number)
    if not empty_hole_numbers:
        await manager.switch_to(all_states.game.end)
    else:
        context.dialog_data.update(empty_holes=empty_hole_numbers)
        await manager.switch_to(all_states.game.empty_holes)
