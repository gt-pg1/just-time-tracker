from datetime import datetime
import calendar


class TimeTracker:
    def __init__(self, category, task, comment, date_start=None, date_end=None, rowid=None):
        self.category = category
        self.task = task if task is not None else None
        self.comment = comment if comment is not None else None
        if date_start is not None:
            self.date_start = date_start
        else:
            date_now = datetime.now()
            datetime_tuple = date_now.utctimetuple()
            self.date_start = calendar.timegm(datetime_tuple)
        self.date_end = date_end if date_end is not None else None
        self.rowid = rowid if rowid is not None else None

        self.data = {'category': self.category,
                     'task': self.task,
                     'comment': self.comment,
                     'date_start': self.date_start,
                     'date_end': self.date_end,
                     'rowid': self.rowid}

    def __repr__(self):
        return f'{self.category}, {self.task}, {self.comment}, {self.date_start}, {self.date_end}, {self.rowid}'
