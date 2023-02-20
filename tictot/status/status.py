from enum import Enum


class AppStatus(str, Enum):
    STARTED = "started"
    STOPPED = "stopped"
