from textual import events
from textual.widgets import TextArea


demo_code = (
    "def bubble_sort(array):\n"
    "    n = len(array)\n"
    "    for i in range(n - 1):\n"
    "        for j in range(0, n - i - 1):\n"
    "            if array[j] > array[j + 1]:\n"
    "                array[j], array[j + 1] = array[j + 1], array[j]\n"
)


class Code(TextArea, inherit_bindings=False):
    """Display a greeting."""

    _inherit_bindings = False
    DEFAULT_CSS = """
    Code {
        padding: 1 2;
        background: $panel;
        border: $secondary tall;
        content-align: center middle;
    }
    """

    BINDINGS = []

    def on_mount(self) -> None:
        self.user_input = ""
        self.script = demo_code
        self.language = "python"
        self.theme = "dracula"
        self.read_only = True
        self.text = self.script

    def get_character(self, event: events.Key) -> str:
        if event.key == "enter":
            return "\n"
        elif event.key == "tab":
            return "    "
        else:
            if event.is_printable:
                return event.character
            return ""

    def on_end(self) -> None:
        self.app.exit(0)

    def _on_key(self, event: events.Key) -> None:
        if event.key == "backspace":
            return

        character: str = self.get_character(event)

        user_input = self.user_input + character
        is_match = user_input == self.script[: len(user_input)]
        is_end = user_input == self.script

        if is_end:
            self.on_end()

        if is_match:
            self.user_input = user_input
            if event.key == "tab":
                self.move_cursor_relative(rows=0, columns=4)
            else:
                self.action_cursor_right()

        else:
            self.app.bell()
