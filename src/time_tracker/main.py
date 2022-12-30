from datetime import datetime
import pandas as pd


class TimerError(Exception):
    pass


class Timer:
    # __init__ = start
    def __init__(self, start):
        if not isinstance(start, datetime):
            raise TypeError('Start can be only datetime data type')
        self.__start = start
        self.str_start = datetime.strftime(self.__start, 'on %d.%m.%Y at %H:%M:%S')
        self.__finish = None
        self.str_finish = None

    @property
    def start(self):
        return self.__start

    @property
    def finish(self):
        if self.__finish is None:
            raise TimerError('Value must be assigned before the call')
        return self.__finish

    @finish.setter
    def finish(self, value):
        if self.__finish is None:
            if not isinstance(value, datetime):
                raise TypeError('Finish can be only datetime data type')
            elif value < self.__start:
                raise TimerError('Value must be bigger than start time')
            else:
                self.__finish = value
        else:
            raise TimerError('Value cannot be assigned a second time')

    def __str__(self):
        return f'Started {self.str_start}' + (f', finished {self.str_finish}' if self.__finish else '')


class Tracker:
    df = pd.DataFrame(columns=['Activity', 'Start date and time', 'Finish date and time', 'Duration'])

    def __init__(self, username):
        if not isinstance(username, str):
            raise TypeError('Username can only be a string value')
        self.username = username

        self.name, self.timer = input('What are you doing?\n'), Timer(datetime.now())
        while not self.name:
            self.name = input('You must enter the name of the activity\n')

        print(self.timer)

        self.made = True
        while self.made:
            input('Press Enter if task is finished...')
            self.timer.finish = datetime.now()
            self.made = False

        # TODO: что-то придумать с периодами между сменой активности (не завершать активность, а именно сменять, т.е.
        #  логику "Press Enter if task is finished..." изменить полностью
        self.delta = self.timer.finish - self.timer.start
        self.duration = self.delta.total_seconds()

        Tracker.df.loc[len(Tracker.df)] = [
            self.name,
            self.timer.start,
            self.timer.finish,
            self.duration
        ]

        # print(Tracker.df)

    def __str__(self):
        return str(self.timer)


class Writer:
    def __init__(self, tracker):
        if not isinstance(tracker, Tracker):
            raise TypeError('Can only work with an object of Tracker class')

        # TODO: постоянно удаляет и перезаписывает файл. Нужно пофиксить, чтобы не мучать жесткий диск
        with pd.ExcelWriter(f'data/{tracker.username}.xlsx', datetime_format="YYYY-MM-DD HH:MM:SS") as writer:
            tracker.df.to_excel(writer, index=False)


while True:
    task = Tracker('Ilya')
    Writer(task)
