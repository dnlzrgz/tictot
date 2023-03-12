import csv

import click
from sqlalchemy.orm import Session

from tictot.config import Config
from tictot.db import DB
from tictot.db.crud import get_time_entries_with_task_name


@click.command(help="Export data from the database to a csv file.")
@click.argument("file", type=click.Path(exists=False))
def export(file: str):
    config = Config()
    db = DB(url=config.DB_PATH)

    export_csv(db.session, file)


def export_csv(session: Session, filename: str):
    """Export data from the database to a CSV file."""
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "task", "start time", "end time"])

        for entry, task in get_time_entries_with_task_name(session):
            writer.writerow([entry.id, task, entry.start_time, entry.end_time])
