from textual.app import App, ComposeResult
from textual.widgets import Footer, Header

from tictot.store import AppStatus, Store
from tictot.widgets.timer import Timer


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
        timer = self.query_one(Timer)
        if (
            self.store.status == AppStatus.STOPPED
            or self.store.status == AppStatus.IDLE
        ):
            self.add_class("counting")
            timer.start()
        elif self.store.status == AppStatus.STARTED:
            self.remove_class("counting")
            timer.stop()

    def action_reset_timer(self) -> None:
        timer = self.query_one(Timer)
        timer.reset()

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        yield Footer()
        yield Timer()


if __name__ == "__main__":
    app = TictotApp()
    app.run()
