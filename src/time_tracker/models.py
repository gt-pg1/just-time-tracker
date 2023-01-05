from datetime import datetime
import calendar


class TimeTracker:
    def __init__(self, category, task, comment, date_added=None, date_completed=None, rowid=None):
        self.category = category
        self.task = task if task is not None else None
        self.comment = comment if comment is not None else None
        if date_added is not None:
            self.date_added = date_added
        else:
            date_now = datetime.now()
            datetime_tuple = date_now.utctimetuple()
            self.date_added = calendar.timegm(datetime_tuple)
        self.date_completed = date_completed if date_completed is not None else None
        self.rowid = rowid if rowid is not None else None

    def __repr__(self):
        return f'{self.category}, {self.task}, {self.comment}, {self.date_added}, {self.date_completed}, {self.rowid}'
