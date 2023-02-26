from datetime import datetime

from textual.app import App, ComposeResult
from textual.reactive import reactive
from textual.widgets import Button, Footer, Header, Input

from tictot.config import Config
from tictot.db import DB, Base
from tictot.db.crud import (
    create_task,
    create_time_entry,
    get_time_entries_by_date,
    update_time_entry_end_time,
)
from tictot.db.models import TimeEntry
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

    config = Config()

    db = DB(url=config.DB_PATH)
    db_session = db.session
    current_entry = reactive(None)

    status = reactive(AppStatus.IDLE)
    current_task = reactive("")

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        yield Footer()
        yield Timer()
        yield TimeEntries()

    def watch_status(self, status: AppStatus) -> None:
        if status == AppStatus.STARTED:
            self.start_timer()
        elif status == AppStatus.STOPPED:
            self.stop_timer()

    def action_start_timer(self) -> None:
        if self.status == AppStatus.STOPPED:
            self.status = AppStatus.STARTED
        elif self.status == AppStatus.STARTED:
            self.status = AppStatus.STOPPED

    async def action_quit(self) -> None:
        if self.current_entry is not None:
            update_time_entry_end_time(
                self.db_session, self.current_entry.id, datetime.now()
            )

        self.db.close()
        await super().action_quit()

    def on_mount(self) -> None:
        """Create database tables."""
        Base.metadata.create_all(self.db.engine)

        # Create default task
        create_task(self.db_session, task_name="Default")

        # load sessions from database from today
        today_date = datetime.today().strftime("%Y-%m-%d")
        entries = get_time_entries_by_date(self.db_session, date=today_date)
        self.query_one(TimeEntries).add_multiple_entries(entries)

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
        self.status = AppStatus.STARTED
        self.set_focus(None)

    def start_timer(self) -> None:
        self.add_class("counting")
        self.query_one(Timer).start()

        self.query_one("#start").disabled = True
        self.query_one("#stop").disabled = False

        if self.current_task:
            self.add_entry(self.current_task)
        else:
            self.add_entry()

    def stop_timer(self) -> None:
        self.remove_class("counting")
        self.query_one(Timer).stop()

        update_time_entry_end_time(
            self.db_session, self.current_entry.id, datetime.now()
        )

        self.query_one(TimeEntries).update_latest_entry(
            self.current_entry.start_time, datetime.now()
        )

        self.query_one("#stop").disabled = True
        self.query_one("#start").disabled = False

    def add_entry(self, task_name: str = "Default") -> None:
        now = datetime.now()

        task = create_task(self.db_session, task_name)
        time_entry = TimeEntry(task_id=task.id, start_time=datetime.now())
        self.current_entry = time_entry

        create_time_entry(self.db_session, time_entry)
        self.query_one(TimeEntries).add_new_entry(now, task_name)
