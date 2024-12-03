from textual.widgets import Static


class LinkToCode(Static):
    DEFAULT_CSS = """
        LinkToCode {
            color: $text-muted;
            width: auto;
            # content-align: center middle;
            text-opacity: 60%;
            height: auto;
            padding-right: 2;
        }
    """
