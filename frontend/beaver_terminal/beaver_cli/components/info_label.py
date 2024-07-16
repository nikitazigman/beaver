from rich.console import RenderableType
from textual.widgets import Label


class InfoDisplay(Label, inherit_bindings=False):
    DEFAULT_CSS = """
        InfoDisplay {
            color: $text-muted;
            width: auto;
            # content-align: center middle;
            text-opacity: 60%;
            height: auto;
            padding-right: 2;
        }
    """

    def __init__(
        self,
        renderable: RenderableType = "",
        *,
        expand: bool = False,
        shrink: bool = False,
        markup: bool = True,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
        disabled: bool = False,
        prefix: str = "#",
    ):
        self.prefix = prefix
        super().__init__(
            renderable=renderable,
            expand=expand,
            shrink=shrink,
            markup=markup,
            name=name,
            id=id,
            classes=classes,
            disabled=disabled,
        )

    def on_mount(self) -> None:
        self.renderable = f"{self.prefix} {self.renderable}"
