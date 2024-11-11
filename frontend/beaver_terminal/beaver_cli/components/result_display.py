from collections.abc import Generator

from beaver_cli.schemas.statistic import Statistic
from textual.containers import Container
from textual.widget import Widget
from textual.widgets import Label, Sparkline


class ResultDisplay(Container, inherit_css=False):
    DEFAULT_CSS = """
        ResultDisplay {
            align-horizontal: center;
            background: $panel;
            border: tall $accent;
            width: 50%;
            height: 50%;
            padding: 0 2;
        }
    """

    def __init__(
        self,
        *children: Widget,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
        disabled: bool = False,
        statistic: Statistic,
        intervals: int = 20,
    ) -> None:
        super().__init__(
            *children,
            name=name,
            id=id,
            classes=classes,
            disabled=disabled,
        )
        self.statistic = statistic
        self.intervals = intervals

    def compute_average_events_per_minute(self, events: list[float]) -> float:
        statistic = [0] * self.intervals
        step = max(events) / self.intervals
        for event in events:
            index = round(event // step) - 1
            statistic[index] += 1

        return statistic

    def compose(self) -> Generator[Widget, None, None]:
        errors = self.compute_average_events_per_minute(self.statistic.typing_errors)
        events = self.compute_average_events_per_minute(self.statistic.typing_events)
        accuracy = 1 - len(self.statistic.typing_errors) / len(self.statistic.typing_events)
        yield Label(f"Total characters: {len(self.statistic.typing_events)}")
        yield Label(f"Total typos: {len(self.statistic.typing_errors)}")
        yield Label(f"Accuracy: {accuracy:.2%}")
        yield Label("Typing Errors")
        yield Sparkline(data=errors, summary_function=max)
        yield Label("Characters per minute")
        yield Sparkline(data=events, summary_function=max)
