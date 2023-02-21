from textual.app import ComposeResult
from textual.widgets import Label, ListItem, ListView, Static


class Sessions(Static):
    def compose(self) -> ComposeResult:
        yield ListView()

    def add_new_session(self, session: str) -> None:
        self.query_one(ListView).mount(ListItem(Label(session)))
