from dataclasses import dataclass
from enum import Enum


class AppStatus(str, Enum):
    IDLE = "idle"
    STARTED = "started"
    STOPPED = "stopped"


class StoreMeta(type):
    """
    Metaclass for the Store class. This metaclass ensures that only one instance of the Store class is created.
    """

    _instances: dict = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(StoreMeta, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


@dataclass
class Store(metaclass=StoreMeta):
    """
    A singleton class that stores the state of the app.
    """

    work_duration = 45 * 60
    break_duration = 15 * 60
    status = AppStatus.IDLE

    def update_status(self, status: AppStatus):
        self.status = status
