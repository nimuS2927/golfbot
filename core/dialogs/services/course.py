from typing import Dict, Union, List, Any

from aiohttp import ClientSession
from pydantic import ValidationError
from requests import HTTPError

from core.dialogs.schemas.courses import Course, CreateCourse, UpdateCourse, UpdateCoursePartial
from core.dialogs.services.base import BaseService


class CourseService(BaseService):
    _model = Course

    async def get_course_by_id(
            self,
            session: ClientSession,
            course_id: int
    ) -> Course:
        headers = await self.create_headers(session=session)
        async with session.get(
            self.api_urls.get_course_by_id(course_id),
            headers=headers,
        ) as response:
            if response.status == 200:
                obj_dict = await response.json()
                return self._model.model_validate(obj_dict)
            if response.status == 422:
                raise ValidationError('Invalid course id')
            raise HTTPError('Server error')

    async def get_courses_all(
            self,
            session: ClientSession,
    ) -> List[Course]:
        headers = await self.create_headers(session=session)
        async with session.get(
            self.api_urls.get_courses(),
            headers=headers,
        ) as response:
            if response.status == 200:
                objs_dict = await response.json()
                return [self._model.model_validate(dict_data) for dict_data in objs_dict]
            if response.status == 422:
                raise ValidationError('Invalid request')
            raise HTTPError('Server error')

    async def get_course_by_name(
            self,
            session: ClientSession,
            course_name: str
    ) -> Course:
        headers = await self.create_headers(session=session)
        async with session.post(
            self.api_urls.post_course_by_name(),
            headers=headers,
            json={'name': course_name}
        ) as response:
            if response.status == 200:
                obj_dict = await response.json()
                return self._model.model_validate(obj_dict)
            if response.status == 422:
                raise ValidationError('Invalid course id')
            raise HTTPError('Server error')

    async def create_course(
            self,
            session: ClientSession,
            data: CreateCourse
    ) -> Course:
        headers = await self.create_headers(session=session)
        async with session.post(
            self.api_urls.post_course(),
            headers=headers,
            json=data,
        ) as response:
            if response.status == 201:
                obj_dict = await response.json()
                return self._model.model_validate(obj_dict)
            if response.status == 422:
                raise ValidationError('Invalid course fields')
            raise HTTPError('Server error')

    async def update_course(
            self,
            session: ClientSession,
            course_id: int,
            data: UpdateCourse
    ) -> Course:
        headers = await self.create_headers(session=session)
        async with session.put(
            self.api_urls.put_course_by_id(course_id),
            headers=headers,
            json=data,
        ) as response:
            if response.status == 200:
                obj_dict = await response.json()
                return self._model.model_validate(obj_dict)
            if response.status == 422:
                raise ValidationError('Invalid course fields')
            raise HTTPError('Server error')

    async def partial_update_course(
            self,
            session: ClientSession,
            course_id: int,
            data: UpdateCoursePartial
    ) -> Course:
        headers = await self.create_headers(session=session)
        async with session.patch(
            self.api_urls.patch_course_by_id(course_id),
            headers=headers,
            json=data,
        ) as response:
            if response.status == 200:
                obj_dict = await response.json()
                return self._model.model_validate(obj_dict)
            if response.status == 422:
                raise ValidationError('Invalid course fields')
            raise HTTPError('Server error')

    async def delete_course(
            self,
            session: ClientSession,
            course_id: int
    ) -> str:
        headers = await self.create_headers(session=session)
        async with session.delete(
            self.api_urls.delete_course_by_id(course_id),
            headers=headers,
        ) as response:
            if response.status == 204:
                return await response.json()
            if response.status == 422:
                raise ValidationError('Invalid course id')
            raise HTTPError('Server error')
