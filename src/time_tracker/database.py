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


def update_activity(rowid: int, category: str, task: str, comment: str, date_added: int, date_completed: int):
    data = {'rowid': rowid,
            'category': category,
            'task': task,
            'comment': comment,
            'date_added': date_added,
            'date_completed': date_completed}

    with con:
        cur.execute("SELECT rowid, * FROM activities WHERE rowid=:rowid", data)
        names = tuple(map(lambda x: x[0], cur.description))
        activity = cur.fetchall()
        activity_data = dict(zip(names, *activity))
        write = {'rowid': data['rowid'] if data['rowid'] else activity_data['rowid'],
                 'category': data['category'] if data['category'] else activity_data['category'],
                 'task': data['task'] if data['task'] else activity_data['task'],
                 'comment': data['comment'] if data['comment'] else activity_data['comment'],
                 'date_added': data['date_added'] if data['date_added'] else activity_data['date_added'],
                 'date_completed': data['date_completed'] if data['date_completed'] else activity_data[
                     'date_completed']}

        cur.execute("""UPDATE activities SET category=:category, task=:task, comment=:comment, 
                       date_added=:date_added, date_completed=:date_completed WHERE rowid=:rowid""", write)


def complete_activity(rowid):
    date_now = datetime.now()
    datetime_tuple = date_now.utctimetuple()
    date_completed = calendar.timegm(datetime_tuple)

    with con:
        cur.execute('UPDATE activities SET date_completed=:date_completed WHERE rowid=:rowid',
                    {'date_completed': date_completed, 'rowid': rowid})
