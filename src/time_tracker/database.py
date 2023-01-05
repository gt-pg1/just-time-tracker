import sqlite3
from typing import List
from datetime import datetime
import calendar
from models import TimeTracker


con = sqlite3.connect('activities.db')
cur = con.cursor()


def create_table():
    cur.execute("""CREATE TABLE IF NOT EXISTS activities (
            category TEXT,
            task TEXT,
            comment TEXT,
            date_added INTEGER,
            date_completed INTEGER
            )""")


create_table()


def insert_activity(timetracker: TimeTracker):
    with con:
        data = {'category': timetracker.category, 'task': timetracker.task, 'comment': timetracker.comment,
                'date_added': timetracker.date_added}
        if data['task'] is not None and data['comment'] is not None:
            cur.execute("""INSERT INTO activities (category, task, comment, date_added) 
                        VALUES (:category, :task, :comment, :date_added)""", data)
        elif data['task'] is not None:
            cur.execute("""INSERT INTO activities (category, task, date_added) 
                        VALUES (:category, :task, :date_added)""", data)
        elif data['comment'] is not None:
            cur.execute("""INSERT INTO activities (category, comment, date_added) 
                        VALUES (:category, :comment, :date_added)""", data)
        else:
            cur.execute("""INSERT INTO activities (category, date_added) 
                        VALUES (:category, :date_added)""", data)


def get_all_activities() -> List[TimeTracker]:
    with con:
        cur.execute("""SELECT category, task, comment, date_added, 
                       date_completed, rowid FROM activities ORDER BY date_added""")
        results = cur.fetchall()
    activities = []
    for result in results:
        activities.append(TimeTracker(*result))
    return activities


def delete_activity(rowid):
    with con:
        cur.execute("DELETE FROM activities WHERE rowid=:rowid", {'rowid': rowid})


def update_activity(rowid: int, category: str, task: str):
    with con:
        if category is not None and category is not None:
            cur.execute("UPDATE activities SET category=:category, task=:task WHERE rowid=:rowid",
                        {'category': category, 'task': task, 'rowid': rowid})
        elif category is not None:
            cur.execute("UPDATE activities SET category=:category WHERE rowid=:rowid",
                        {'category': category, 'rowid': rowid})
        elif task is not None:
            cur.execute("UPDATE activities SET task=:task WHERE rowid=:rowid",
                        {'task': task, 'rowid': rowid})


def complete_activity(rowid):
    date_now = datetime.now()
    datetime_tuple = date_now.utctimetuple()
    date_completed = calendar.timegm(datetime_tuple)

    with con:
        cur.execute('UPDATE activities SET date_completed=:date_completed WHERE rowid=:rowid',
                    {'date_completed': date_completed, 'rowid': rowid})
