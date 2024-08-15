from pathlib import Path

from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Center, ScrollableContainer
from textual.screen import ModalScreen
from textual.widgets import Footer, Markdown, Static


HELP_CONTENT_PATH = Path(__file__).parent.parent / "components/resources/help.md"

class HelpScreen(ModalScreen[None]):
    CSS_PATH = "css/help_screen.tcss"

    BINDINGS = [Binding("escape", "app.pop_screen", "Close", show=True)]


    def compose(self) -> ComposeResult:
        with ScrollableContainer(id="help_screen_container"):
            yield Center(Static("Help", id="help_screen_title"))
            with open(HELP_CONTENT_PATH) as help_file:
                yield Markdown(help_file.read())
            yield Footer()
