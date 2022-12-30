from datetime import datetime


class TimerError(Exception):
    pass


class Timer:
    def __init__(self):
        self.__start = datetime.now()
        self.str_start = datetime.strftime(self.__start, 'on %d.%m.%Y at %H:%M:%S')
        self.__finish = None

    @property
    def finish(self):
        if self.__finish is None:
            self.__finish = datetime.now()
            self.str_finish = datetime.strftime(self.__finish, 'on %d.%m.%Y at %H:%M:%S')
            return 'Done'
        else:
            raise TimerError('This deed is already done')

    def __str__(self):
        return f'Started {self.str_start}' + (f', finished {self.str_finish}' if self.__finish else '')


class Tracker:
    def __init__(self):
        self.name, self.timer = input('What are you doing?\n'), Timer()
        print(self.timer)
        self.made = True
        while self.made:
            input('Press Enter if task is finished...')
            self.timer.finish
            self.made = False

    def __str__(self):
        return str(self.timer)


a = Tracker()
print(a)
