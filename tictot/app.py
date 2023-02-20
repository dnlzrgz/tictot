from textual.app import App, ComposeResult
from textual.reactive import reactive
from textual.widgets import Button, Footer, Header, Input

from tictot.status import AppStatus
from tictot.widgets import Timer


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

    status = reactive(AppStatus.STOPPED)
    current_task = reactive("")

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        yield Footer()
        yield Timer()

    def watch_status(self, status: AppStatus) -> None:
        if status == AppStatus.STARTED:
            self.status = status
            self.add_class("counting")
            self.query_one(Timer).start()
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
