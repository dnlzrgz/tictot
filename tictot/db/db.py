from dataclasses import dataclass

from sqlalchemy import Engine, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker


@dataclass
class DB:
    url: str = "sqlite:///./tictot.db"
    engine: Engine = create_engine(url, connect_args={"check_same_thread": False})
    session: Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)()

    def close(self) -> None:
        self.session.close()
        self.engine.dispose()


Base = declarative_base()
