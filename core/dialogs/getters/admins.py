from typing import List, Optional

from aiogram_dialog import DialogManager

from core.dialogs.schemas.courses import Course
from core.dialogs.schemas.tournaments import Tournament
from core.dialogs.utils.pluralization_rules import pluralization
from core.dialogs.schemas.admins import AdminSchemas
from core.dialogs.services import AdminService, all_services
from core.main.keyboards.buttons import MainKB, AdminKB

Object = AdminSchemas


class AdminGetter:

    def __init__(self):
        self.service = AdminService()
        self.__singular = 'admin'
        self.__plural = pluralization(self.singular)

    @property
    def singular(self):
        return self.__singular

    @property
    def plural(self):
        return self.__plural

    @staticmethod
    async def get_tournaments(
            dialog_manager: DialogManager,
            **middleware_data
    ):
        # region получаем промежуточные данные
        middleware_data = dialog_manager.middleware_data
        session = middleware_data.get('session')
        dialog_data = dialog_manager.dialog_data
        kind_of = dialog_data.get('kind_of')
        # endregion
        # region Получаем турниры на основании нажатой кнопки
        if kind_of == AdminKB.nearest_tournaments[1]:
            tournaments: List[Tournament] = await all_services.tournament.get_tournament_nearest(
                session=session
            )
        elif kind_of == AdminKB.all_tournaments[1]:
            tournaments: List[Tournament] = await all_services.tournament.get_tournaments_all(
                session=session
            )
        else:
            raise ValueError('kind_of не сохранилось в контексте')
        # endregion
        return {'tournaments': tournaments}

    @staticmethod
    async def get_tournament(
            dialog_manager: DialogManager,
            **middleware_data
    ):
        # region получаем промежуточные данные
        middleware_data = dialog_manager.middleware_data
        session = middleware_data.get('session')
        dialog_data = dialog_manager.dialog_data
        tournament = dialog_data.get('tournament')
        tournament_id = dialog_data.get('tournament_id')
        update_status = dialog_data.get('update_status')
        # endregion
        # region Получаем турнир из БД если его нет в диалоге
        if tournament_id:
            if not tournament or update_status:
                tournament = await all_services.tournament.get_tournament_by_id(
                    session=session,
                    tournament_id=tournament_id,
                    course_status=True
                )
                dialog_data.update(tournament=tournament)
        # endregion
        # region Получаем переменные и добавляем если их нет в диалоге
        tournament_name = dialog_data.get('tournament_name')
        tournament_type = dialog_data.get('tournament_type')
        tournament_flights = dialog_data.get('tournament_flights')
        course_name = dialog_data.get('course_name')
        id_course = dialog_data.get('id_course')
        start_day = dialog_data.get('start_day')
        end_day = dialog_data.get('end_day')
        hcp = dialog_data.get('hcp')

        if not tournament_name:
            tournament_name = tournament.name if tournament else ' '
        if not tournament_type:
            tournament_type = tournament.type if tournament else ' '
        if not tournament_flights:
            tournament_flights = tournament.max_flights if tournament else ' '
        if not course_name:
            course_name = tournament.course.name if tournament else ' '
        if not id_course:
            id_course = tournament.course.id if tournament else ' '
        if not start_day:
            start_day = tournament.start if tournament else ' '
            start_day = ' '.join(start_day.split('T'))
        if not end_day:
            end_day = tournament.end if tournament else ' '
            end_day = ' '.join(end_day.split('T'))
        if not hcp:
            hcp = tournament.hcp if tournament else ' '
        dialog_data.update(
            tournament_name=tournament_name,
            tournament_type=tournament_type,
            tournament_flights=tournament_flights,
            course_name=course_name,
            id_course=id_course,
            start_day=start_day,
            end_day=end_day,
            hcp=hcp,
        )
        # endregion
        return {
            'tournament': tournament,
            'tournament_name': tournament_name,
            'tournament_type': tournament_type,
            'tournament_flights': tournament_flights,
            'course_name': course_name,
            'start_day': start_day,
            'end_day': end_day,
            'hcp': hcp,
        }

    @staticmethod
    async def get_tournament_types(
            dialog_manager: DialogManager,
            **middleware_data
    ):
        types = [
            ('stableford', 0),
            ('stroke play', 1),
            ('stroke play nett', 2),
        ]
        dialog_manager.dialog_data.update(types=types)
        return {'types': types}

    @staticmethod
    async def get_courses_name(
            dialog_manager: DialogManager,
            **middleware_data
    ):
        middleware_data = dialog_manager.middleware_data
        session = middleware_data.get('session')
        courses: Optional[List[Course]] = await all_services.course.get_courses_all(
            session=session,
        )
        if not courses:
            return []
        course_names = [(course.name, course.id, i) for i, course in enumerate(courses)]
        dialog_manager.dialog_data.update(course_names=course_names)
        return {'course_names': course_names}


g_admin = AdminGetter()
