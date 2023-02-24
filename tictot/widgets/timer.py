from time import monotonic

from textual.app import ComposeResult
from textual.containers import Container
from textual.reactive import reactive
from textual.widgets import Button, Input, Static


class Display(Static):
    """
    A widget to display the remaining time.
    """

    start_time = reactive(monotonic)
    time = reactive(0.0)
    total = reactive(0.0)

    def on_mount(self) -> None:
        """
        Event handler called when widget is added to the app.
        """
        self.update_timer = self.set_interval(1 / 60, self.update_time, pause=True)

    def update_time(self) -> None:
        """Method to update time to current."""
        self.time = self.total + (monotonic() - self.start_time)

    def watch_time(self, time: float) -> None:
        """Called when the time attribute changes."""
        minutes = (time // 60) % 60
        seconds = time % 60

        self.update(f"{minutes:02.0f}:{seconds:02.0f}")

    def start(self) -> None:
        """Method to start (or resume) time updating."""
        self.start_time = monotonic()
        self.update_timer.resume()

    def stop(self) -> None:
        """Method to stop the time display updating."""
        self.update_timer.pause()
        self.total += monotonic() - self.start_time
        self.time = self.total

    def reset(self) -> None:
        """Method to reset the time display."""
        self.total = 0.0
        self.time = 0.0


class TaskInput(Static):
    """
    Input widget to enter the current task name.
    """

    def compose(self) -> ComposeResult:
        yield Input(value=None, placeholder="Current task name", id="input")


class Timer(Static):
    """
    A widget to display the stopwatch.
    """

    def compose(self) -> ComposeResult:
        """
        Create child widgets for the timer.
        """
        yield Display()
        yield Container(
            Button("Start", id="start", variant="success", disabled=False),
            TaskInput(),
            Button("Stop", id="stop", variant="error", disabled=True),
            classes="buttons",
        )

    def start(self) -> None:
        """
        Passtrough method to start the timer.
        """
        self.query_one(Display).start()

    def stop(self) -> None:
        """
        Passtrough method to stop the timer.
        """
        self.query_one(Display).stop()
        self.query_one(Display).reset()
