from threading import Lock
from Observers.IObserver import Subject


class SingletonMeta(type):

    _instans = None
    _lock = Lock()

    def __call__(self, *args, **kwargs):
        with self._lock:
            if not self._instans:
                self._instans = super().__call__(*args, **kwargs)
        return self._instans


class DataBase(Subject):
    robot = []
    task_list_robot = []
    task_list_sort = []

    __metaclass__ = SingletonMeta

    def attach(self, observer):
        DataBase.robot.append(observer)

    def notify(self):
        for observer in DataBase.robot:
            observer[0].update(self)

    def detach(self, observer):
        DataBase.robot.remove(observer)

    def listupdate(self):
        DataBase.notify(self)
