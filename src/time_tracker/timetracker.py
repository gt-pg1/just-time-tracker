import datetime
import calendar
from typing import *

from models import TimeTracker
from database import insert_activity, get_activities, delete_activity, update_activity, complete_activity


def add(category: str, task=None, comment=None, date_start=None, date_end=None):
    activity = TimeTracker(category, task, comment, date_start, date_end)
    insert_activity(activity)


def delete(rowid):
    delete_activity(rowid)


def update(rowid, category=None, task=None, comment=None, date_start=None, date_end=None):
    update_activity(rowid, category, task, comment, date_start, date_end)


def complete(rowid):
    complete_activity(rowid)


def show(start=0, end=10413795661):
    activities = get_activities(start, end)
    for activity in activities:
        print(activity)


def show_by_day(year, month, day):
    date_start = datetime.datetime(year, month, day, 0, 0, 0)
    date_start_tuple = date_start.utctimetuple()
    date_start_unix = calendar.timegm(date_start_tuple)

    date_end = datetime.datetime(year, month, day, 23, 59, 59)
    date_end_tuple = date_end.utctimetuple()
    date_end_unix = calendar.timegm(date_end_tuple)

    show(date_start_unix, date_end_unix)


def second_start():
    date_start = datetime.datetime(2023, 1, 3, 10, 0, 0)
    date_start_tuple = date_start.utctimetuple()
    date_start_unix = calendar.timegm(date_start_tuple)

    date_end = datetime.datetime.now()
    date_end_tuple = date_end.utctimetuple()
    date_end_unix = calendar.timegm(date_end_tuple)
    add('Test activity')


if __name__ == '__main__':
    second_start()
