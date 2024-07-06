from textual import events
from textual.events import Click, MouseDown, MouseMove, MouseUp
from textual.message import Message
from textual.widgets import TextArea


class Code(TextArea, inherit_bindings=False):
    """Display a greeting."""

    DEFAULT_CSS = """
    Code {
        background: $panel;
        border: none;
        margin: 0;
        padding: 1 0;
        content-align: center middle;
        text-opacity: 100%;

        &:focus {
            border: none;
        }
    }   
    """

    BINDINGS = []

    class Running(Message):
        """Color selected message."""

        def __init__(self, running: bool) -> None:
            self.running = running
            super().__init__()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user_input = ""
        self.read_only = True

    def on_mount(self) -> None:
        self.disable_messages(MouseDown, MouseUp, MouseMove, Click)

    def get_character(self, event: events.Key) -> str:
        if event.key == "enter":
            return "\n"
        elif event.key == "tab":
            return "    "

        if not event.is_printable:
            raise ValueError("Not a printable character")

        return event.character

    def on_mouse_down(self, event: events.MouseDown) -> None:
        event.stop()

    async def _on_mouse_up(self, event: events.MouseDown) -> None:
        event.stop()

    async def _on_mouse_move(self, event: events.MouseMove) -> None:
        event.stop()

    async def _on_click(self, event: events.Click) -> None:
        event.stop()

    def start(self) -> None:
        self.post_message(self.Running(running=True))

    def stop(self) -> None:
        self.post_message(self.Running(running=False))

    def on_key(self, event: events.Key) -> None:
        try:
            if not self.user_input:
                self.start()

            character: str = self.get_character(event)

            user_input = self.user_input + character
            is_match = user_input == self.text[: len(user_input)]
            is_end = user_input == self.text

            if is_end:
                self.stop()

            if not is_match:
                raise ValueError("Invalid input")

            self.user_input = user_input
            if event.key == "tab":
                self.move_cursor_relative(rows=0, columns=4)
            else:
                self.action_cursor_right()

        except ValueError:
            self.app.bell()
