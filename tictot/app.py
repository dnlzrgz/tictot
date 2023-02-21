from textual.app import App, ComposeResult
from textual.reactive import reactive
from textual.widgets import Button, Footer, Header, Input

from tictot.db import DB, Base
from tictot.status import AppStatus
from tictot.widgets import Sessions, Timer


class TictotApp(App):
    """
    A Textual app for time management.
    """

    TITLE = "Tictot"
    CSS_PATH = "./style.css"
    BINDINGS = [
        ("s", "start_timer", "Start/Stop"),
        ("r", "reset_timer", "Reset"),
        ("d", "toggle_dark", "Toggle dark mode"),
        ("q", "quit", "Quit"),
    ]

    db = DB()

    status = reactive(AppStatus.STOPPED)
    current_task = reactive("")

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        yield Footer()
        yield Timer()
        yield Sessions()

    def watch_status(self, status: AppStatus) -> None:
        if status == AppStatus.STARTED:
            self.status = status
            self.add_class("counting")
            self.query_one(Timer).start()

            if self.current_task:
                self.query_one(Sessions).add_new_session(self.current_task)
            else:
                self.query_one(Sessions).add_new_session("Default")
        elif status == AppStatus.STOPPED:
            self.status = status
            self.remove_class("counting")
            self.query_one(Timer).stop()

    def action_start_timer(self) -> None:
        if self.status == AppStatus.STOPPED:
            self.status = AppStatus.STARTED
        elif self.status == AppStatus.STARTED:
            self.status = AppStatus.STOPPED

    def action_reset_timer(self) -> None:
        self.query_one(Timer).reset()

    def on_mount(self) -> None:
        """Create database tables."""
        Base.metadata.create_all(self.db.engine)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        button_id = event.button.id

        if button_id == "start":
            self.status = AppStatus.STARTED
        elif button_id == "stop":
            self.status = AppStatus.STOPPED
        elif button_id == "reset" and self.status == AppStatus.STOPPED:
            self.query_one(Timer).reset()

    def on_input_submitted(self, event: Input.Submitted) -> None:
        """Handle input submission."""
        self.current_task = event.value
