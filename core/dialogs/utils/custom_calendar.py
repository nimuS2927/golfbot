from dataclasses import dataclass
from datetime import datetime, date

from aiogram_dialog.widgets.kbd import Calendar
from aiogram_dialog.widgets.kbd import (
    Calendar, CalendarScope, CalendarUserConfig, CalendarConfig
)

calendar_config = CalendarConfig(min_date=date.today())
