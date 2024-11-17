from time import monotonic

from textual.reactive import reactive
from textual.widgets import Label


class TimeDisplay(Label):
    DEFAULT_CSS = """
        TimeDisplay {
            # content-align: center middle;
            text-opacity: 60%;
            height: auto;
        }
        .started TimeDisplay {
            text-opacity: 100%;
        }
    """

    start_time = reactive(monotonic)
    time = reactive(0.0)

    def on_mount(self) -> None:
        """Event handler called when widget is added to the app."""
        self.update_timer = self.set_interval(1 / 60, self.update_time, pause=True)

    def update_time(self) -> None:
        """Method to update the time to the current time."""
        self.time = monotonic() - self.start_time

    def watch_time(self, time: float) -> None:
        """Called when the time attribute changes."""
        minutes, seconds = divmod(time, 60)
        hours, minutes = divmod(minutes, 60)
        self.update(f"{minutes:02.0f}:{seconds:02.0f}")

    def start(self) -> None:
        """Method to start (or resume) time updating."""
        self.start_time = monotonic()
        self.update_timer.resume()

    def stop(self) -> None:
        """Method to stop the time display updating."""
        self.update_timer.pause()

    def reset(self) -> None:
        """Method to reset the time display to zero."""
        self.time = 0
