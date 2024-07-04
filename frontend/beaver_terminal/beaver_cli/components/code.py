from textual import events
from textual.widgets import TextArea


class Code(TextArea, inherit_bindings=False):
    """Display a greeting."""

    _inherit_bindings = False
    DEFAULT_CSS = """
    Code {
        padding: 1 2;
        background: $panel;
        border: $secondary tall;
        content-align: center middle;
        text-opacity: 100%;
    }
    """

    BINDINGS = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user_input = ""
        self.read_only = True

    def get_character(self, event: events.Key) -> str:
        if event.key == "enter":
            return "\n"
        elif event.key == "tab":
            return "    "

        if not event.is_printable:
            raise ValueError("Not a printable character")

        return event.character

    def on_end(self) -> None:
        ...

    def _on_key(self, event: events.Key) -> None:
        try:
            character: str = self.get_character(event)

            user_input = self.user_input + character
            is_match = user_input == self.text[: len(user_input)]
            is_end = user_input == self.text

            if is_end:
                self.on_end()

            if not is_match:
                raise ValueError("Invalid input")

            self.user_input = user_input
            if event.key == "tab":
                self.move_cursor_relative(rows=0, columns=4)
            else:
                self.action_cursor_right()

        except ValueError:
            self.app.bell()
