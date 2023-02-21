from sqlalchemy.orm import Session

from tictot.db import models


def create_task(db: Session, task: models.Task) -> models.Task:
    """
    Create a new task. If task already exists, return the existing task.
    """
    db_task: models.Task | None = get_task(db, task["id"])
    if db_task is not None:
        return db_task

    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def get_task(db: Session, task_id: int) -> models.Task:
    """
    Get a task by its ID.
    """
    return db.query(models.Task).filter(models.Task.id == task_id).first()


def get_task_by_name(db: Session, task_name: str) -> models.Task:
    """
    Get a task by its name.
    """
    return db.query(models.Task).filter(models.Task.name == task_name).first()


def remove_task(db: Session, task_id: int) -> None:
    """
    Remove a task and all time entries associated with it.
    """
    # remove the task
    db.query(models.Task).filter(models.Task.id == task_id).delete()
    # remove all time entries associated with this task
    db.query(models.TimeEntry).filter(models.TimeEntry.task_id == task_id).delete()

    db.commit()


def update_task(db: Session, task_id: int, task: models.Task) -> models.Task:
    """
    Update a task. If task does not exist, create it.
    """
    db_task: models.Task | None = (
        db.query(models.Task).filter(models.Task.id == task_id).first()
    )
    if db_task is None:
        return create_task(db, task)

    db_task.name = task.name
    db.commit()
    db.refresh(db_task)
    return db_task


def create_time_entry(db: Session, time_entry: models.TimeEntry) -> models.TimeEntry:
    """
    Create a new time entry. If time entry already exists, return the existing time entry.
    """
    db_time_entry: models.TimeEntry | None = get_time_entry(db, time_entry["id"])
    if db_time_entry is not None:
        return db_time_entry

    db.add(time_entry)
    db.commit()
    db.refresh(time_entry)
    return time_entry


def get_time_entry(db: Session, time_entry_id: int) -> models.TimeEntry:
    """
    Get a time entry by its ID.
    """
    return (
        db.query(models.TimeEntry).filter(models.TimeEntry.id == time_entry_id).first()
    )


def get_time_entries(db: Session, task_id: int) -> list[models.TimeEntry]:
    """
    Get all time entries for a task.
    """
    return db.query(models.TimeEntry).filter(models.TimeEntry.task_id == task_id).all()


def get_time_entries_by_date(
    db: Session, task_id: int, date: str
) -> list[models.TimeEntry]:
    """
    Get all time entries for a task on a specific date.
    """
    return (
        db.query(models.TimeEntry)
        .filter(models.TimeEntry.task_id == task_id)
        .filter(models.TimeEntry.start_time.like(f"{date}%"))
        .all()
    )


def remove_time_entry(db: Session, time_entry_id: int) -> None:
    """
    Remove a time entry.
    """
    db.query(models.TimeEntry).filter(models.TimeEntry.id == time_entry_id).delete()
    db.commit()


def update_time_entry(
    db: Session, time_entry_id: int, time_entry: models.TimeEntry
) -> models.TimeEntry:
    """
    Update a time entry. If time entry does not exist, create it.
    """
    db_time_entry: models.TimeEntry | None = (
        db.query(models.TimeEntry).filter(models.TimeEntry.id == time_entry_id).first()
    )
    if db_time_entry is None:
        return create_time_entry(db, time_entry)

    db_time_entry.start_time = time_entry.start_time
    db_time_entry.end_time = time_entry.end_time
    db.commit()
    db.refresh(db_time_entry)
    return db_time_entry
