from datetime import datetime

from textual.app import App, ComposeResult
from textual.reactive import reactive
from textual.widgets import Button, Footer, Header, Input

from tictot.db import DB, Base
from tictot.db.crud import (
    create_task,
    create_time_entry,
    get_task_by_name,
    get_time_entries_by_date,
)
from tictot.db.models import Task, TimeEntry
from tictot.status import AppStatus
from tictot.widgets import TimeEntries, Timer


class TictotApp(App):
    """
    A Textual app for time management.
    """

    TITLE = "Tictot"
    CSS_PATH = "./style.css"
    BINDINGS = [
        ("s", "start_timer", "Start/Stop"),
        ("d", "toggle_dark", "Toggle dark mode"),
        ("q", "quit", "Quit"),
    ]

    db = DB()
    local_session = db.session

    sessions = reactive([])
    status = reactive(AppStatus.STOPPED)
    current_task = reactive("")

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        yield Footer()
        yield Timer()
        yield TimeEntries()

    def watch_status(self, status: AppStatus) -> None:
        if status == AppStatus.STARTED:
            self.status = status
            self.add_class("counting")
            self.query_one(Timer).start()

            self.query_one("#start").disabled = True
            self.query_one("#stop").disabled = False

            if self.current_task:
                db_task = create_task(self.local_session, Task(name=self.current_task))
                time_entry = TimeEntry(task_id=db_task.id, start_time=datetime.now())
                create_time_entry(self.local_session, time_entry)
                self.sessions.append(time_entry.task)
                self.query_one(TimeEntries).add_new_session(db_task.name)
            else:
                default_task = get_task_by_name(self.local_session, "Default")
                time_entry = TimeEntry(
                    task_id=default_task.id, start_time=datetime.now()
                )
                create_time_entry(self.local_session, time_entry)
                self.sessions.append(time_entry.task)
                self.query_one(TimeEntries).add_new_session("Default")
        elif status == AppStatus.STOPPED:
            self.status = status
            self.remove_class("counting")
            self.query_one(Timer).stop()

            self.query_one("#stop").disabled = True
            self.query_one("#start").disabled = False

    def watch_sessions(self, sessions: list) -> None:
        print(len(sessions))

    def action_start_timer(self) -> None:
        if self.status == AppStatus.STOPPED:
            self.status = AppStatus.STARTED
        elif self.status == AppStatus.STARTED:
            self.status = AppStatus.STOPPED

    def on_mount(self) -> None:
        """Create database tables."""
        Base.metadata.create_all(self.db.engine)

        # Create default task
        create_task(self.local_session, Task(name="Default"))

        # load sessions from database from today
        today_date = datetime.today().strftime("%Y-%m-%d")
        self.sessions = get_time_entries_by_date(self.local_session, date=today_date)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        button_id = event.button.id

        if button_id == "start":
            self.status = AppStatus.STARTED
        elif button_id == "stop":
            self.status = AppStatus.STOPPED

    def on_input_submitted(self, event: Input.Submitted) -> None:
        """Handle input submission."""
        self.current_task = event.value
