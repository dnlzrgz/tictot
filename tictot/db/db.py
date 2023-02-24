from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


class DB:
    def __init__(self, url: str = "sqlite://:memory:") -> None:
        self.url: str = url
        self.engine = create_engine(url, connect_args={"check_same_thread": False})
        self.session = sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine
        )()

    def close(self) -> None:
        self.session.close()
        self.engine.dispose()


Base = declarative_base()
