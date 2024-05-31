from pydantic import BaseModel, ConfigDict


class CourseBase(BaseModel):
    name: str


class CreateCourse(CourseBase):
    pass


class UpdateCourse(CourseBase):
    pass


class UpdateCoursePartial(CourseBase):
    name: str = None


class Course(CourseBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
