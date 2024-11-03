from textual import events
from textual.events import Click, MouseDown, MouseMove, MouseUp
from textual.message import Message
from textual.reactive import Reactive, reactive
from textual.widgets import TextArea


class UserStartTyping(Message):
    """User has started the code."""


class UserCompletedCode(Message):
    """User has completed the code."""


class UserErrorEvent(Message):
    """User has made a typo."""


class UserCorrectEvent(Message):
    """User has made a typo."""


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
    user_input: Reactive = reactive("", always_update=False, init=False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.read_only = True

    def on_mount(self) -> None:
        self.disable_messages(MouseDown, MouseUp, MouseMove, Click)

    def move_cursor_to_user_input_position(self, user_input: str) -> None:
        user_input = user_input.split("\n")
        row = len(user_input) - 1
        column = len(user_input[-1])
        self.move_cursor((row, column))

    def watch_user_input(self, user_input: str) -> None:
        self.move_cursor_to_user_input_position(user_input)
        self.post_message(UserCorrectEvent())

        if self.text == user_input:
            self.post_message(UserCompletedCode())

    def get_insert_value(self, event: events.Key) -> str:
        mapping = {
            "enter": "\n",
            "tab": "    ",
        }

        if value := mapping.get(event.key):
            return value

        if not event.is_printable:
            raise ValueError("Not a printable character")

        return event.character

    def on_key(self, event: events.Key) -> None:
        try:
            not self.user_input and self.post_message(UserStartTyping())
            character: str = self.get_insert_value(event)
            user_input = self.user_input + character

            if user_input != self.text[: len(user_input)]:
                raise ValueError("Invalid input")

            self.user_input = user_input

        except ValueError:
            self.post_message(UserErrorEvent())
            self.app.bell()
