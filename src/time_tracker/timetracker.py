from models import TimeTracker
from database import insert_activity, get_all_activities, delete_activity, update_activity, complete_activity
from typing import *


def add(category: str, task=None, comment=None):
    activity = TimeTracker(category, task, comment)
    insert_activity(activity)


def delete(rowid):
    delete_activity(rowid)


def update(rowid, category=None, task=None):
    update_activity(rowid, category, task)


def complete(rowid):
    complete_activity(rowid)


def show():
    activities = get_all_activities()
    for activity in activities:
        print(activity)


def first_start():
    add('TEST', 'TTEST', 'Writen')
    delete(12)
    show()
    update(5, 'NewTEST')
    complete(13)


if __name__ == '__main__':
    first_start()
