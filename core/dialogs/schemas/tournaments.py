from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field
from typing import Annotated, Optional, List
from annotated_types import MinLen, MaxLen
from pydantic.types import NaiveDatetime


class TournamentBase(BaseModel):
    name: Annotated[str, MinLen(3), MaxLen(300)]
    type: str
    max_flights: int
    status: bool = False
    id_course: int
    start: NaiveDatetime = Field(..., examples=['fmt: YYYY-MM-DD or YYYY-MM-DD HH:MM'])
    end: NaiveDatetime = Field(..., examples=['fmt: YYYY-MM-DD or YYYY-MM-DD HH:MM'])
    hcp: Optional[int] = None


class CreateTournament(TournamentBase):
    pass


class UpdateTournament(TournamentBase):
    pass


class UpdateTournamentPartial(TournamentBase):
    name: Optional[Annotated[str, MinLen(3), MaxLen(300)]] = None
    type: str = None
    max_flights: Optional[int] = None
    id_course: int = None
    start: NaiveDatetime = Field(None, examples=['fmt: YYYY-MM-DD or YYYY-MM-DD HH:MM'])
    end: NaiveDatetime = Field(None, examples=['fmt: YYYY-MM-DD or YYYY-MM-DD HH:MM'])
    hcp: Optional[int] = None


class Tournament(TournamentBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
