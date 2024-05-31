from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field
from typing import Annotated, Optional, List
from annotated_types import MinLen, MaxLen
from pydantic.types import NaiveDatetime

from typing import TYPE_CHECKING

from .courses import Course


class TournamentBase(BaseModel):
    name: Annotated[str, MinLen(3), MaxLen(300)]
    type: str
    max_flights: int
    status: bool = False
    id_course: int
    start: str = Field(..., examples=['fmt: YYYY-MM-DD or YYYY-MM-DD HH:MM'])
    end: str = Field(..., examples=['fmt: YYYY-MM-DD or YYYY-MM-DD HH:MM'])
    hcp: Optional[int] = None


class CreateTournament(TournamentBase):
    pass


class UpdateTournament(TournamentBase):
    pass


class UpdateTournamentPartial(TournamentBase):
    name: Optional[Annotated[str, MinLen(3), MaxLen(300)]] = None
    type: Optional[str] = None
    max_flights: Optional[int] = None
    id_course: Optional[int] = None
    start: Optional[str] = None
    end: Optional[str] = None
    hcp: Optional[int] = None


class Tournament(TournamentBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


class TournamentWithCourse(TournamentBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    course: Course
