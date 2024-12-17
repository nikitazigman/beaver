from textual.widgets import Static


class ErrorMessage(Static):
    DEFAULT_CSS = """
        ErrorMessage {
            background: $panel;
            padding: 1 2;
            align: center middle;
            width: 100%;
        }

        #error-container {
            background: $boost;
            padding: 2 4;
            border: heavy $error;
            width: 90%;
            max-width: 90%;
        }

        #error {
            margin-bottom: 1;
            text-style: bold;
            content-align-horizontal: center;
            content-align-vertical: middle;
            width: 100%;
            text-align: center;
        }
    """

    def __init__(self, message: str):
        super().__init__()
        self.message = message

    def compose(self):
        with Static(id="error-container"):
            yield Static(f"Error: {self.message}\n\nPress ^n to retry", id="error")
