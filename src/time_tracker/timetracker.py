from datetime import datetime, timedelta
import calendar
import time
from typing import *

from models import TimeTracker
from database import insert_activity, get_activities, delete_activity, update_activity, complete_activity


def add(
        category: str, task: Optional[str] = None, comment: Optional[str] = None,
        date_start: Optional[int] = None, date_end: Optional[int] = None
) -> None:
    activity = TimeTracker(category, task, comment, date_start, date_end)
    insert_activity(activity)


def delete(rowid: int) -> None:
    delete_activity(rowid)


def update(
        rowid: int, category: Optional[str] = None, task: Optional[str] = None, comment: Optional[str] = None,
        date_start: Optional[int] = None, date_end: Optional[int] = None
) -> None:
    update_activity(rowid, category, task, comment, date_start, date_end)


def complete(rowid: int) -> None:
    complete_activity(rowid)


def show(start: int = 0, end: int = 10413795661) -> None:
    activities: List[TimeTracker] = get_activities(start, end)
    for activity in activities:
        print(activity)


def show_by_day(year: int, month: int, day: int) -> None:
    date_start: datetime = datetime(year, month, day, 0, 0, 0)
    date_start_tuple: time.struct_time = date_start.utctimetuple()
    date_start_unix: int = calendar.timegm(date_start_tuple)

    date_end: datetime = datetime(year, month, day, 23, 59, 59)
    date_end_tuple: time.struct_time = date_end.utctimetuple()
    date_end_unix: int = calendar.timegm(date_end_tuple)

    show(date_start_unix, date_end_unix)


def second_start() -> None:
    date_start = datetime(2023, 1, 3, 15, 0, 0)
    date_start_tuple = date_start.utctimetuple()
    date_start_unix = calendar.timegm(date_start_tuple)

    date_end = datetime(2023, 1, 5, 10, 0, 0)
    date_end_tuple = date_end.utctimetuple()
    date_end_unix = calendar.timegm(date_end_tuple)

    show()


if __name__ == '__main__':
    second_start()
