from textual.widgets import Static


class TagDisplay(Static):
    DEFAULT_CSS = """
        TagDisplay {
            color: $text-muted;
            width: auto;
            # content-align: center middle;
            text-opacity: 60%;
            height: auto;
            padding-right: 2;
        }
    """

    def on_mount(self) -> None:
        self.renderable = f"# Tags: {self.renderable}"
