from textual.widgets import Static


class LanguageDisplay(Static):
    DEFAULT_CSS = """
        LanguageDisplay {
            color: $text-muted;
            width: auto;
            text-opacity: 60%;
            height: auto;
            padding-right: 2;
        }
    """

    def on_mount(self) -> None:
        self.renderable = f"# Language: {self.renderable}"
