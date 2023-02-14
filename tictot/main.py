from dataclasses import dataclass
from enum import Enum
from time import monotonic

from textual.app import App, ComposeResult
from textual.containers import Container
from textual.reactive import reactive
from textual.widgets import Button, Footer, Header, Static


class TimerStatus(str, Enum):
    IDLE = "idle"
    STARTED = "started"
    STOPPED = "stopped"


@dataclass
class DefaultConfig:
    work_duration = 45 * 60
    break_duration = 15 * 60


class TimerDisplay(Static):
    """Widget to display the elapsed time."""

    config = DefaultConfig()

    status = reactive(TimerStatus.IDLE)
    start_time = reactive(monotonic)
    time = reactive(config.work_duration)
    total = reactive(config.work_duration)

    def on_mount(self) -> None:
        """Event handler called when widget is added to the app."""
        self.update_timer = self.set_interval(1 / 60, self.update_time, pause=True)

    def update_time(self) -> None:
        """Method to update the time to the current time."""
        self.time = self.total - (monotonic() - self.start_time)

    def watch_time(self, time: float) -> None:
        """Called when the time attributes change."""
        mins, secs = divmod(time, 60)
        _, mins = divmod(mins, 60)
        self.update(f"{mins:02,.0f}:{secs:02.0f}")

    def start(self) -> None:
        """Method to start (or resume) timer."""
        self.status = TimerStatus.STARTED
        self.start_time = monotonic()
        self.update_timer.resume()

    def stop(self) -> None:
        """Method to stop the time display updating."""
        self.status = TimerStatus.STOPPED
        self.update_timer.pause()
        self.total -= monotonic() - self.start_time
        self.time = self.total

    def reset(self) -> None:
        """Method to reset the time display to zero."""
        self.total = self.config.work_duration
        self.time = self.config.work_duration


class Timer(Static):
    """A Timer widget."""

    def compose(self) -> ComposeResult:
        """Create child widgets for the stopwatch."""
        yield TimerDisplay("45:00")
        yield Container(
            Button("Start", id="start", variant="success"),
            Button("Stop", id="stop", variant="error"),
            Button("Reset", id="reset", variant="default"),
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Event handler called when a button is pressed."""
        button_id = event.button.id
        time_display = self.query_one(TimerDisplay)

        if button_id == "start":
            time_display.start()
            self.add_class("counting")
        elif button_id == "stop":
            time_display.stop()
            self.remove_class("counting")
        elif button_id == "reset":
            time_display.reset()


class TictotApp(App):
    """A Textual based App for time management."""

    CSS_PATH = "./style.css"
    BINDINGS = [
        ("s", "start_timer", "Start/Stop"),
        ("r", "reset_timer", "Reset"),
        ("d", "toggle_dark", "Toggle dark mode"),
        ("q", "quit", "Quit"),
    ]

    def action_start_timer(self) -> None:
        time_display = self.query_one(TimerDisplay)
        if (
            time_display.status == TimerStatus.STOPPED
            or time_display.status == TimerStatus.IDLE
        ):
            self.add_class("counting")
            time_display.start()
        elif time_display.status == TimerStatus.STARTED:
            self.remove_class("counting")
            time_display.stop()

    def action_reset_timer(self) -> None:
        time_display = self.query_one(TimerDisplay)
        time_display.reset()

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        yield Footer()
        yield Timer()


if __name__ == "__main__":
    app = TictotApp()
    app.run()
