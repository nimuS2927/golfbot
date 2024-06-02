from typing import Any, List, Optional, Dict

from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button

from core.dialogs.utils.game_rules import stroke_play_nett, stableford
from core.dialogs.schemas.holes import Hole
from core.dialogs.schemas.scores import CreateScore, Score, UpdateScorePartial
from core.dialogs.schemas.totalscores import TotalScore, TotalForFirstCreate, UpdateTotalScorePartial
from core.dialogs.schemas.tournaments import Tournament
from core.dialogs.schemas.users import User
from core.dialogs.states import all_states
from core.dialogs.services import all_services
from core.dialogs.utils import getters_obj_from_list, emoji


async def on_list_available_tournament(
        callback: CallbackQuery,
        button: Button,
        manager: DialogManager,
):
    # region Получаем промежуточные данные и входные переменные
    middleware_data = manager.middleware_data
    session = middleware_data.get('session')
    user_tg_id = callback.from_user.id
    # endregion
    # region Запрашиваем турниры доступные для игры
    objs: List[Tournament] = await all_services.tournament.get_tournaments_for_game(
        session=session,
        user_tg_id=user_tg_id
    )
    # endregion
    if not objs:
        await manager.start(state=all_states.game.empty)  # Турниров нет
    else:
        await manager.start(state=all_states.game.choice)  # Турниры есть


async def on_choice_tournament(
        callback: CallbackQuery,
        button: Button,
        manager: DialogManager,
        item_id: int,
):
    # region Получаем контекст и входные переменные
    context = manager.current_context()
    session = manager.middleware_data.get('session')
    user: User = await all_services.user.get_user_by_tg_id(session=session, tg_id=callback.from_user.id)
    context = manager.current_context()
    context.dialog_data.update(user=user.model_dump())
    # endregion
    # region Запрашиваем турнир
    tournament: Tournament = await all_services.tournament.get_tournament_by_id(session=session, tournament_id=item_id)
    # endregion
    # region Запрашиваем лунки для поля на котором проводится турнир
    holes: List[Hole] = await all_services.hole.get_holes_by_course_id(
        session=session, course_id=tournament.id_course)
    # endregion
    # region Проверяем наличие в диалоге счетов лунок и общего счета для пользователя
    scores_list: Optional[List[Score]] = context.dialog_data.get('scores')
    total_score: Optional[TotalScore] = context.dialog_data.get('total_score')
    # endregion
    # region если в диалоге счетов нет, значит проверяем в базе
    if scores_list is None:
        scores_list: List[Score] = await all_services.score.get_scores_by_id_tournament_and_id_user(
            session=session,
            id_tournament=tournament.id,
            id_user=user.id,
        )
        total_score: Optional[TotalScore] = await all_services.totalscores.get_totalscore_by_id_tournament_and_id_user(
            session=session,
            id_tournament=tournament.id,
            id_user=user.id,
        )
        # region если в базе нет Общего счета создаем его и счета для каждой лунки
        if not total_score:
            create_total_score: TotalForFirstCreate = TotalForFirstCreate(
                id_tournament=item_id,
                id_user=user.id,
                total=0,
            )
            total_score: TotalScore = await all_services.totalscores.create_totalscore(
                session=session,
                data=create_total_score.model_dump()
            )
        if not scores_list:
            create_score_list = []
            for hole in holes:
                create_score: CreateScore = CreateScore(
                    id_tournament=item_id,
                    id_hole=hole.id,
                    id_user=user.id,
                    id_total_score=total_score.id,
                )
                create_score_list.append(create_score.model_dump())
            scores_list: List[Score] = await all_services.score.create_scores(
                session=session,
                data=create_score_list
            )
        # endregion
    # endregion
    # region Обновляем данные диалога
    context.dialog_data.update(
        tournament_id=item_id,
        tournament=tournament,
        scores=scores_list,
        user=user,
        total_score=total_score,
        holes=holes
    )
    # endregion
    await manager.switch_to(all_states.game.start)


async def on_choice_holes(
        callback: CallbackQuery,
        button: Button,
        manager: DialogManager,
        item_id: int,
):
    # region Получаем сессию, запрашиваем Лунку по ID и обновляем данные диалога
    context = manager.current_context()
    session = manager.middleware_data.get('session')
    hole: Hole = await all_services.hole.get_hole_by_id(session=session, hole_id=item_id)
    context.dialog_data.update(hole_id=item_id, hole=hole)
    # endregion
    await manager.switch_to(all_states.game.result)


async def on_entered_impacts(
        m: Message,
        widget: Any,
        manager: DialogManager,
        item_id: str,
):
    item_id = int(item_id)

    # region Получаем промежуточные и входные данные
    # region Сессия
    middleware_data = manager.middleware_data
    session = middleware_data.get('session')
    # endregion
    # region Данные из контекста (Общий счет, Счета по лункам, турнир, пользователь, лунки)
    context = manager.current_context()
    impacts_list = context.dialog_data.get('impacts_list')
    impacts = impacts_list[item_id][1]
    scores_dict: List[dict] = context.dialog_data.get('scores')
    scores: List[Score] = [Score.model_validate(i_dict) for i_dict in scores_dict]
    total_score_dict: dict = context.dialog_data.get('total_score')
    total_score: TotalScore = TotalScore.model_validate(total_score_dict)
    tournament_dict: dict = context.dialog_data.get('tournament')
    tournament: Tournament = Tournament.model_validate(tournament_dict)
    user_dict: dict = context.dialog_data.get('user')
    user: User = User.model_validate(user_dict)
    hole_cur_dict: dict = context.dialog_data.get('hole')
    hole_cur: Hole = Hole.model_validate(hole_cur_dict)
    holes_dict: List[dict] = context.dialog_data.get('holes')
    holes: List[Hole] = [Hole.model_validate(i_dict) for i_dict in holes_dict]
    # endregion
    # endregion
    # region Проверяем в данных диалога наличие заполненных лунок
    holes_ids: Optional[Dict[int, list[int, int, int, str]]] = context.dialog_data.get('holes_ids')
    # region Заполняем данные счета по текущей лунке
    score: Score = getters_obj_from_list.get_obj_by_attribute(
        objs=scores,
        attribute='id_hole',
        value=hole_cur.id
    )
    old_impacts = None
    if score.impacts:
        old_impacts = score.impacts
    score.impacts = int(impacts)

    holes_ids[hole_cur.id] = [
        score.impacts,
        hole_cur.par,
        hole_cur.difficulty,
        emoji.for_holes(score.impacts - hole_cur.par)
    ]
    data_update_score_partial: UpdateScorePartial = UpdateScorePartial(
        impacts=int(impacts)
    )
    score = await all_services.score.partial_update_score(
        session=session,
        score_id=score.id,
        data=data_update_score_partial.model_dump(exclude_unset=True)
    )
    # endregion
    # region Считаем общий счет и обновляем данные в БД
    handicap = round(user.handicap)
    total_cur = total_score.total
    if not total_cur:
        total_score.total = 0
        total_cur = total_score.total
    # region Формат stableford
    if tournament.type == 'stableford':
        if not old_impacts:
            points = stableford(
                impacts=score.impacts,
                par=hole_cur.par,
                index=hole_cur.difficulty,
                handicap=handicap,
                hcp=tournament.hcp,
            )
            total_cur += points
        else:
            pre_points = stableford(
                impacts=old_impacts,
                par=hole_cur.par,
                index=hole_cur.difficulty,
                handicap=handicap,
                hcp=tournament.hcp,
            )
            points = stableford(
                impacts=score.impacts,
                par=hole_cur.par,
                index=hole_cur.difficulty,
                handicap=handicap,
                hcp=tournament.hcp,
            )
            total_cur += points - pre_points
        total_score.total = total_cur
    # endregion
    # region Формат stroke play и stroke play nett
    else:
        if not old_impacts:
            total_cur += score.impacts
        else:
            total_cur += score.impacts - old_impacts
        if tournament.type == 'stroke play':
            total_score.total = total_cur
        elif tournament.type == 'stroke play nett':
            if total_score.total == 0:
                total_score.total = stroke_play_nett(total_impacts=total_cur, handicap=handicap, hcp=tournament.hcp)
            else:
                total_score.total += total_cur
    # endregion
    data_update_totalscore_partial: UpdateTotalScorePartial = UpdateTotalScorePartial(
        total=total_cur
    )
    await all_services.totalscores.partial_update_totalscore(
        session=session,
        totalscore_id=total_score.id,
        data=data_update_totalscore_partial.model_dump(exclude_unset=True)
    )
    context.dialog_data.update(
        scores=scores,
        totalscore=total_score,
        holes_ids=holes_ids)
    # endregion
    await manager.switch_to(all_states.game.start)


async def on_completed_game(
        callback: CallbackQuery,
        button: Button,
        manager: DialogManager,
):
    # region Получаем промежуточные и входные данные
    # region Сессия
    middleware_data = manager.middleware_data
    session = middleware_data.get('session')
    # endregion
    # region Данные из контекста
    context = manager.current_context()
    scores_list: Optional[List[Score]] = context.dialog_data.get('scores')
    # endregion
    # endregion
    # region Проверяем не заполненные лунки
    empty_hole_numbers = []
    for sc in scores_list:
        if not sc.impacts:
            hole: Hole = await all_services.hole.get_hole_by_id(session=session, hole_id=sc.id_hole)
            empty_hole_numbers.append(hole.number)
    # endregion
    if not empty_hole_numbers:
        await manager.switch_to(all_states.game.end)
    else:
        context.dialog_data.update(empty_holes=empty_hole_numbers)
        await manager.switch_to(all_states.game.empty_holes)


async def on_top(
        callback: CallbackQuery,
        button: Button,
        manager: DialogManager,
):
    # region Получаем промежуточные и входные данные
    # region Сессия
    middleware_data = manager.middleware_data
    session = middleware_data.get('session')
    # endregion
    # region Данные из контекста
    context = manager.current_context()
    tournament_id: int = context.dialog_data.get('tournament_id')
    # endregion
    # endregion
    # region Получаем турнир с общими счетами каждого игрока
    tournament_dict = await all_services.tournament.get_tournament_for_top(
        session=session,
        tournament_id=int(tournament_id)
    )
    totalscores = tournament_dict.get('totalscores')
    # endregion
    if not totalscores:
        await manager.switch_to(all_states.game.empty_top)
    else:
        context.dialog_data.update(totalscores=totalscores, tournament_type=tournament_dict['type'])
        await manager.switch_to(all_states.game.top)


