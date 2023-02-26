from pathlib import Path


class SingletonConfig(type):
    """
    Singleton metaclass for Config class.
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonConfig, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Config(metaclass=SingletonConfig):
    """
    Configuration class for tictot.

    Attributes:
        DEBUG (bool): Whether to run in debug mode.
        DB_PATH (str): Path to the database.
    """

    def __init__(self, debug: bool = False) -> None:
        self.DEBUG = debug
        self.DB_PATH = "sqlite://"

        if not self.DEBUG:
            home_dir = Path.home()
            config_folder = home_dir / ".tictot"
            config_folder.mkdir(exist_ok=True)

            db_path = config_folder / "tictot.db"
            self.DB_PATH = f"sqlite:///{db_path}"
