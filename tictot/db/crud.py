from datetime import datetime

from sqlalchemy.orm import Session

import tictot.db.models as models


def create_task(db: Session, task_name: str) -> models.Task:
    """
    Create a new task. If task already exists, return the existing task.
    """
    db_task = get_task_by_name(db, task_name=task_name)
    if db_task is not None:
        return db_task

    task = models.Task(name=task_name)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def get_task(db: Session, task_id: int) -> models.Task | None:
    """
    Get a task by its ID.
    """
    return db.query(models.Task).filter(models.Task.id == task_id).first()


def get_task_by_name(db: Session, task_name: str) -> models.Task | None:
    """
    Get a task by its name.
    """
    return db.query(models.Task).filter(models.Task.name == task_name).first()


def remove_task(db: Session, task_id: int) -> None:
    """
    Remove a task and all time entries associated with it.
    """
    db.query(models.Task).filter(models.Task.id == task_id).delete()
    db.query(models.TimeEntry).filter(models.TimeEntry.task_id == task_id).delete()

    db.commit()


def update_task(db: Session, task_name: str, new_name: str) -> models.Task:
    """
    Update a task. If task does not exist, create it.
    """
    task = get_task_by_name(db, task_name=task_name)
    if task is None:
        return create_task(db, new_name)

    task.name = new_name
    db.commit()
    db.refresh(task)
    return task


def create_time_entry(db: Session, time_entry: models.TimeEntry) -> models.TimeEntry:
    """
    Create a new time entry.
    """
    db.add(time_entry)
    db.commit()
    db.refresh(time_entry)
    return time_entry


def get_time_entry(db: Session, entry_id: int) -> models.TimeEntry | None:
    """
    Get a time entry by its ID.
    """
    return db.query(models.TimeEntry).filter(models.TimeEntry.id == entry_id).first()


def get_time_entries(db: Session) -> list[models.TimeEntry]:
    """
    Get all time entries.
    """
    return db.query(models.TimeEntry).all()


def get_time_entries_by_task(db: Session, task_id: int) -> list[models.TimeEntry]:
    """
    Get all time entries for a task.
    """
    return db.query(models.TimeEntry).filter(models.TimeEntry.task_id == task_id).all()


def get_time_entries_by_date(db: Session, date: str) -> list[models.TimeEntry]:
    """
    Get all time entries for a task on a specific date.
    """
    return (
        db.query(models.TimeEntry)
        .filter(models.TimeEntry.start_time.like(f"{date}%"))
        .all()
    )


def remove_time_entry(db: Session, entry_id: int) -> None:
    """
    Remove a time entry.
    """
    db.query(models.TimeEntry).filter(models.TimeEntry.id == entry_id).delete()
    db.commit()


def update_time_entry(
    db: Session, old_entry: models.TimeEntry, updated_entry: models.TimeEntry
) -> models.TimeEntry:
    """
    Update a time entry. If time entry does not exist, create it.
    """
    entry = get_time_entry(db, entry_id=old_entry.id)
    if entry is None:
        return create_time_entry(db, updated_entry)

    entry.start_time = updated_entry.start_time
    entry.end_time = updated_entry.end_time
    db.commit()
    db.refresh(entry)
    return entry


def update_time_entry_end_time(
    db: Session, entry_id: int, end_time: datetime
) -> models.TimeEntry | None:
    """
    Update the end time of a time entry.
    """
    entry = get_time_entry(db, entry_id=entry_id)
    if entry is None:
        return None

    entry.end_time = end_time
    db.commit()
    db.refresh(entry)
    return entry
