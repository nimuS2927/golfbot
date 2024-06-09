from typing import List, Optional, Union, Any, Dict
from core.dialogs.schemas.holes import Hole
from core.dialogs.schemas.tournaments import Tournament
from core.dialogs.schemas.scores import Score
from core.dialogs.schemas.totalscores import TotalScore
from core.dialogs.schemas.users import User
from core.dialogs.schemas.admins import AdminSchemas

OBJS = [Hole, Tournament, Score, TotalScore, User, AdminSchemas]


def get_obj_by_attribute(objs: List[Union[*OBJS]], attribute: str, value: Any) -> Optional[Union[*OBJS]]:
    for obj in objs:
        if obj.__getattribute__(attribute) == value:
            return obj
    return None


def get_obj_by_key(objs: List[Dict[str, Any]], key: str, value: Any) -> Optional[Dict[str, Any]]:
    if objs:
        for obj in objs:
            if obj.get(key) == value:
                return obj
    return None
