from datetime import datetime

from textual.app import ComposeResult
from textual.containers import Container
from textual.widgets import Label, ListItem, ListView, Static


class TimeEntries(Static):
    def compose(self) -> ComposeResult:
        yield Container(
            Label(datetime.today().strftime("%a, %b %d")),
            Label(),
            Label("01:25 hours"),
            classes="header",
        )
        yield ListView(
            ListItem(
                Label(datetime.now().strftime("%H:%M")),
                Label("Buy Tomatoes"),
                Label(""),
            ),
            ListItem(
                Label(datetime.now().strftime("%H:%M")),
                Label("Buy Tomatoes"),
                Label(datetime.now().strftime("%H:%M")),
            ),
        )

    def add_new_session(self, session: str) -> None:
        self.query_one(ListView).mount(ListItem())
