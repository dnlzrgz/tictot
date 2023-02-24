from enum import Enum


class AppStatus(str, Enum):
    IDLE = ("idle",)
    STARTED = "started"
    STOPPED = "stopped"
