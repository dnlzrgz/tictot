from datetime import datetime

from textual.app import ComposeResult
from textual.containers import Container
from textual.reactive import reactive
from textual.widgets import Label, ListItem, ListView, Static


class TimeEntries(Static):
    total_time = reactive(0)

    def compose(self) -> ComposeResult:
        yield Container(
            Label(datetime.today().strftime("%a, %b %d")),
            Label(),
            Label("00:00 hours"),
            classes="total",
            id="total",
        )
        yield ListView()

    def watch_total_time(self) -> None:
        hours = self.total_time // 3600
        minutes = (self.total_time % 3600) // 60

        self.query_one("#total").children[2].update(
            f"{hours:02.0f}:{minutes:02.0f} hours"
        )

    def add_multiple_entries(self, entries: list) -> None:
        for entry in entries:
            if entry.end_time is None:
                continue

            start_time = entry.start_time
            task_name = entry.task.name
            end_time = entry.end_time

            self.query_one(ListView).mount(
                ListItem(
                    Label(start_time.strftime("%H:%M")),
                    Label(task_name),
                    Label(end_time.strftime("%H:%M")),
                )
            )

            self.total_time += (end_time - start_time).seconds

    def add_new_entry(self, start_time: datetime, task: str) -> None:
        self.query_one(ListView).mount(
            ListItem(
                Label(start_time.strftime("%H:%M")),
                Label(task),
                Label(""),
            )
        )

    def update_latest_entry(self, start_time: datetime, end_time: datetime) -> None:
        entries = self.query(ListItem)
        if len(entries) == 0:
            return

        last_entry = entries.last()
        last_entry.children[2].update(end_time.strftime("%H:%M"))

        self.total_time += (end_time - start_time).seconds
