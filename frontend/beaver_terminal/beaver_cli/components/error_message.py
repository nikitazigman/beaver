
from textual.widgets import Static


class ErrorMessage(Static):
    DEFAULT_CSS = """
        ErrorMessage {
            background: $panel;
            padding: 1 2;
            align: center middle;

        }
        #error {
            margin-bottom: 1;
            text-style: bold;
            content-align-horizontal: center;
            content-align-vertical: middle;
            width: auto;
            text-align: center;
        }
    """

    def __init__(self, message: str):
        super().__init__()
        self.message = message

    def compose(self):
        yield Static(f"Error: {self.message}\n\nPress ^n to retry", id="error")
