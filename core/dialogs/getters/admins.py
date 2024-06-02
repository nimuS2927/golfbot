from typing import List, Optional, Dict, Any

from aiogram_dialog import DialogManager

from core.dialogs.schemas.courses import Course
from core.dialogs.schemas.holes import Hole
from core.dialogs.schemas.tournaments import Tournament
from core.dialogs.states import all_states
from core.dialogs.utils.pluralization_rules import pluralization
from core.dialogs.schemas.admins import AdminSchemas
from core.dialogs.services import AdminService, all_services
from core.main.keyboards.buttons import MainKB, AdminKB
from core.dialogs.utils.getters_obj_from_list import get_obj_by_attribute

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
        tournament_name = dialog_data.get('tournament_name')
        tournament_type = dialog_data.get('tournament_type')
        tournament_flights = dialog_data.get('tournament_flights')
        course_name = dialog_data.get('course_name')
        id_course = dialog_data.get('id_course')
        start_day = dialog_data.get('start_day')
        end_day = dialog_data.get('end_day')
        hcp = dialog_data.get('hcp')
        # endregion
        # region Получаем турнир из БД если его нет в диалоге
        if tournament_id:
            if not tournament or update_status:
                tournament = await all_services.tournament.get_tournament_by_id(
                    session=session,
                    tournament_id=tournament_id,
                    course_status=True
                )
                tournament_name = tournament.name if tournament else ''
                tournament_type = tournament.type if tournament else ''
                tournament_flights = tournament.max_flights if tournament else ''
                course_name = tournament.course.name if tournament else ''
                id_course = tournament.course.id if tournament else ''
                start_day = tournament.start if tournament else ''
                start_day = ' '.join(start_day.split('T'))
                end_day = tournament.end if tournament else ''
                end_day = ' '.join(end_day.split('T'))
                hcp = tournament.hcp if tournament else ''
                dialog_data.update(update_status=False)
        # endregion
        # region Получаем переменные и добавляем если их нет в диалоге
        if not tournament_name:
            tournament_name = tournament.name if tournament else ''
        if not tournament_type:
            tournament_type = tournament.type if tournament else ''
        if not tournament_flights:
            tournament_flights = tournament.max_flights if tournament else ''
        if not course_name:
            course_name = tournament.course.name if tournament else ''
        if not id_course:
            id_course = tournament.course.id if tournament else ''
        if not start_day:
            start_day = tournament.start if tournament else ''
            start_day = ' '.join(start_day.split('T'))
        if not end_day:
            end_day = tournament.end if tournament else ''
            end_day = ' '.join(end_day.split('T'))
        if not hcp:
            hcp = tournament.hcp if tournament else ''
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

    @staticmethod
    async def get_users(
            dialog_manager: DialogManager,
            **middleware_data
    ):
        # region получаем промежуточные данные
        middleware_data = dialog_manager.middleware_data
        session = middleware_data.get('session')
        context = dialog_manager.current_context()
        # endregion
        # region Получаем пользователей из БД
        users = await all_services.user.get_users_all(
            session=session,
        )
        context.dialog_data.update(
            users=users,
        )
        # endregion
        return {'users': users}

    @staticmethod
    async def get_user(
            dialog_manager: DialogManager,
            **middleware_data
    ):
        # region получаем промежуточные данные
        middleware_data = dialog_manager.middleware_data
        session = middleware_data.get('session')
        context = dialog_manager.current_context()
        user_id = context.dialog_data.get('user_id')
        # endregion
        # region Получаем пользователей из БД
        user = await all_services.user.get_user(
            session=session,
            user_id=user_id
        )
        context.dialog_data.update(
            user=user,
        )
        # endregion
        return {'user': user}

    @staticmethod
    async def get_admins(
            dialog_manager: DialogManager,
            **middleware_data
    ):
        # region получаем промежуточные данные
        middleware_data = dialog_manager.middleware_data
        session = middleware_data.get('session')
        context = dialog_manager.current_context()
        # endregion
        # region Получаем пользователей из БД
        admins = await all_services.admin.get_admins_all(
            session=session,
        )
        context.dialog_data.update(
            admins=admins,
        )
        # endregion
        return {'admins': admins}

    @staticmethod
    async def get_admin(
            dialog_manager: DialogManager,
            **middleware_data
    ):
        # region получаем промежуточные данные
        middleware_data = dialog_manager.middleware_data
        session = middleware_data.get('session')
        context = dialog_manager.current_context()
        admins = context.dialog_data.get('admins')
        admin_id = context.dialog_data.get('admin_id')
        admin = get_obj_by_attribute(admins, 'id', admin_id)
        # endregion
        # region Получаем пользователей из БД
        context.dialog_data.update(
            admin=admin,
        )
        # endregion
        return {'admin': admin}

    @staticmethod
    async def get_admin_registration(
            dialog_manager: DialogManager,
            **middleware_data
    ):
        # region получаем промежуточные данные
        middleware_data = dialog_manager.middleware_data
        session = middleware_data.get('session')
        context = dialog_manager.current_context()
        login = context.dialog_data.get('login')
        password_1 = context.dialog_data.get('password_1')
        password_2 = context.dialog_data.get('password_2')
        stars_1 = context.dialog_data.get('stars_1')
        stars_2 = context.dialog_data.get('stars_2')
        # endregion
        # region
        login = login if login else ''
        password_1 = password_1 if password_1 else ''
        password_2 = password_2 if password_2 else ''
        stars_1 = stars_1 if stars_1 else ''
        stars_2 = stars_2 if stars_2 else ''
        context.dialog_data.update(
            login=login,
            password_1=password_1,
            password_2=password_2,
            stars_1=stars_1,
            stars_2=stars_2,
        )
        # endregion
        return {'login': login,
                'stars_1': stars_1,
                'stars_2': stars_2,
        }

    @staticmethod
    async def get_courses(
            dialog_manager: DialogManager,
            **middleware_data
    ):
        # region получаем промежуточные данные
        middleware_data = dialog_manager.middleware_data
        session = middleware_data.get('session')
        context = dialog_manager.current_context()
        # endregion
        # region Получаем поля с лунками из диалога
        courses: dict = context.dialog_data.get('courses')
        courses_update = context.dialog_data.get('courses_update')
        if not courses or courses_update:
            courses = await all_services.course.get_courses_with_holes(
                session=session,
            )
            courses_update = False
        courses_list = [(course['id'], course['name']) for course in courses]
        # endregion
        context.dialog_data.update(
            courses_list=courses_list,
            courses_update=courses_update,
        )
        return {'courses': courses, 'courses_list': courses_list}

    @staticmethod
    async def get_holes(
            dialog_manager: DialogManager,
            **middleware_data
    ):
        # region получаем промежуточные данные
        middleware_data = dialog_manager.middleware_data
        session = middleware_data.get('session')
        context = dialog_manager.current_context()
        course = context.dialog_data.get('course')
        # update_holes = context.dialog_data.get('update_holes')

        # endregion
        # # region Получаем поля с лунками из диалога
        # if not update_holes:
        #     holes_dict: List[Dict[str, Any]] = sorted(course['holes'], key=lambda x: x['number'])
        #     holes: List[Hole] = [Hole.model_validate(hole) for hole in holes_dict]
        #     context.dialog_data.update(
        #         holes=holes,
        #     )
        #     return {'holes': holes}
        # # endregion
        # else:
        course_id = course['id']
        course_dict = await all_services.course.get_course_by_id_with_holes(
            session=session,
            course_id=course_id
        )
        holes_dict: List[Dict[str, Any]] = sorted(course_dict['holes'], key=lambda x: x['number'])
        holes: List[Hole] = [Hole.model_validate(hole) for hole in holes_dict]
        context.dialog_data.update(
            holes=holes,
            course=course_dict
        )
        return {'holes': holes}


g_admin = AdminGetter()
