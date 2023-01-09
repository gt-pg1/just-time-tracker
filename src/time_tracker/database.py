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
            date_start INTEGER,
            date_end INTEGER
            )""")


create_table()


def insert_activity(timetracker: TimeTracker):
    with con:
        data = timetracker.data

        if data['date_start'] is None:
            raise TypeError("'date_start' can't be None")

        if not isinstance(data['date_start'], int) or not isinstance(data['date_end'], int):
            raise TypeError("'date_start' and 'date_end' must be an UNIX time format (int)")

        if data['date_end'] and data['date_start'] > data['date_end']:
            raise ValueError("date_start can't be bigger than date_end")

        cur.execute("""INSERT INTO activities (category, task, comment, date_start, date_end) 
                       VALUES (:category, :task, :comment, :date_start, :date_end)""", data)


def get_all_activities() -> List[TimeTracker]:
    with con:
        cur.execute("""SELECT category, task, comment, date_start, date_end, rowid 
                       FROM activities 
                       ORDER BY date_start""")
        results = cur.fetchall()

    activities = []
    for result in results:
        activities.append(TimeTracker(*result))

    return activities


def get_activities(start, end) -> List[TimeTracker]:
    with con:
        cur.execute("""SELECT category, task, comment, date_start, date_end, rowid 
                       FROM activities
                       WHERE date_start >= ? AND date_end <= ?
                       ORDER BY date_start""", (start, end))
        results = cur.fetchall()
    activities = []
    for result in results:
        activities.append(TimeTracker(*result))
    return activities


def delete_activity(rowid):
    with con:
        cur.execute("DELETE FROM activities WHERE rowid=:rowid", {'rowid': rowid})


def update_activity(rowid: int, category: str, task: str, comment: str, date_start: int, date_end: int):
    data = {'rowid': rowid,
            'category': category,
            'task': task,
            'comment': comment,
            'date_start': date_start,
            'date_end': date_end}

    with con:
        cur.execute("SELECT rowid, * FROM activities WHERE rowid=:rowid", data)
        names = tuple(map(lambda x: x[0], cur.description))
        activity = cur.fetchall()
        activity_data = dict(zip(names, *activity))
        write = {'rowid': data['rowid'] if data['rowid'] else activity_data['rowid'],
                 'category': data['category'] if data['category'] else activity_data['category'],
                 'task': data['task'] if data['task'] else activity_data['task'],
                 'comment': data['comment'] if data['comment'] else activity_data['comment'],
                 'date_start': data['date_start'] if data['date_start'] else activity_data['date_start'],
                 'date_end': data['date_end'] if data['date_end'] else activity_data[
                     'date_end']}

        cur.execute("""UPDATE activities 
                       SET category=:category, 
                           task=:task, 
                           comment=:comment, 
                           date_start=:date_start, 
                           date_end=:date_end 
                       WHERE rowid=:rowid""", write)


def complete_activity(rowid):
    date_now = datetime.now()
    datetime_tuple = date_now.utctimetuple()
    date_end = calendar.timegm(datetime_tuple)

    with con:
        cur.execute("UPDATE activities SET date_end=:date_end WHERE rowid=:rowid",
                    {'date_end': date_end, 'rowid': rowid})
