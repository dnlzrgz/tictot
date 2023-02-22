from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from tictot.db import Base


class TimeEntry(Base):
    __tablename__ = "time_entries"

    id = Column(Integer, primary_key=True, index=True)
    start_time = Column(DateTime, index=True, nullable=False)
    end_time = Column(DateTime)
    task_id = Column(Integer, ForeignKey("tasks.id"), nullable=False)

    task = relationship("Task", backref="time_entries")


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
