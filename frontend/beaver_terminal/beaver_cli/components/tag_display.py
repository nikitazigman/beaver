from textual.widgets import Static


class TagDisplay(Static):
    DEFAULT_CSS = """
        TagDisplay {
            color: $text;
            width: auto;
            padding-left: 3;
            # content-align: center middle;
            text-opacity: 60%;
        }
    """
