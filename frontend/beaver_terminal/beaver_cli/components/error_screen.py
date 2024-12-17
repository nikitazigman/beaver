from pathlib import Path

from beaver_cli.components.error_message import ErrorMessage
from textual.app import ComposeResult
from textual.binding import Binding
from textual.screen import ModalScreen
from textual.widgets import Footer, Static


ASSETS_FOLDER_PATH = Path(__file__).parent.parent / "assets"


class ErrorScreen(ModalScreen[None]):
    CSS_PATH: Path = ASSETS_FOLDER_PATH / "error_screen.tcss"  # type: ignore
    BINDINGS: list[Binding] = [
        Binding(key="escape", action="close", description="Close", show=True),
    ]

    def __init__(self, error_message: str) -> None:
        super().__init__()
        self.error_message: str = error_message

    def compose(self) -> ComposeResult:
        yield Static(renderable="Error", id="error_screen_title")
        yield ErrorMessage(message=self.error_message)
        yield Footer()

    def action_close(self) -> None:
        """Close the screen."""
        self.app.pop_screen()
