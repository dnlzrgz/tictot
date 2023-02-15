from time import monotonic

from textual.app import App, ComposeResult
from textual.containers import Container
from textual.reactive import reactive
from textual.widgets import Button, Footer, Header, Static

from tictot.store import AppStatus, Store


class TimerDisplay(Static):
    """
    A widget to display the time remaining.
    """

    store = Store()

    start_time = reactive(monotonic)
    time = reactive(store.work_duration)
    total = reactive(store.work_duration)

    def on_mount(self):
        """
        Called when the widget is mounted into the view.
        """
        self.update_timer = self.set_interval(1 / 60, self.update_time, pause=True)

    def update_time(self):
        """
        Update the time remaining.
        """
        self.time = self.total - (monotonic() - self.start_time)

    def watch_time(self, time: float):
        """
        Watch the time remaining and update the display.
        """
        mins, secs = divmod(time, 60)
        _, mins = divmod(mins, 60)
        self.update(f"{mins:02,.0f}:{secs:02.0f}")

    def start(self):
        """
        Start the timer.
        """
        self.store.update_status(AppStatus.STARTED)

        self.start_time = monotonic()
        self.update_timer.resume()

    def stop(self):
        """
        Stop the timer.
        """
        self.store.update_status(AppStatus.STOPPED)

        self.update_timer.pause()
        self.total -= monotonic() - self.start_time
        self.time = self.total

    def reset(self):
        """
        Reset the timer only if the timer is not running.
        """
        if self.store.status == AppStatus.STARTED:
            return

        self.total = self.store.work_duration
        self.time = self.store.work_duration


class Timer(Static):
    """
    A widget to display the stopwatch.
    """

    def compose(self) -> ComposeResult:
        """
        Create child widgets for the timer.
        """
        yield TimerDisplay("45:00")
        yield Container(
            Button("Start", id="start", variant="success"),
            Button("Stop", id="stop", variant="error"),
            Button("Reset", id="reset", variant="default", disabled=True),
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """
        Handle button presses.
        """
        button_id = event.button.id
        time_display = self.query_one(TimerDisplay)

        if button_id == "start":
            self.add_class("counting")
            time_display.start()
        elif button_id == "stop":
            self.remove_class("counting")
            time_display.stop()
        elif button_id == "reset":
            time_display.reset()


class TictotApp(App):
    """
    A Textual app for time management.
    """

    store = Store()

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
            self.store.status == AppStatus.STOPPED
            or self.store.status == AppStatus.IDLE
        ):
            self.add_class("counting")
            time_display.start()
        elif self.store.status == AppStatus.STARTED:
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
