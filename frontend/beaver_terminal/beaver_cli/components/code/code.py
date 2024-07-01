from beaver_cli.services.code_document import CodeService
from beaver_cli.utils.session import Session
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
    }
    """

    BINDINGS = []

    def on_mount(self) -> None:
        with Session() as session:
            service = CodeService(session=session)
            code_document = service.get_code_document()

        self.user_input = ""
        self.script = code_document.code
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
