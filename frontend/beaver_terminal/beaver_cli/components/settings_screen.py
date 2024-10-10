from pathlib import Path

from beaver_cli.services.language import LanguageService
from beaver_cli.services.tag import TagService
from beaver_cli.utils.session import Session
from textual.app import ComposeResult, on
from textual.binding import Binding
from textual.containers import ScrollableContainer
from textual.screen import ModalScreen
from textual.widgets import Footer, Select, SelectionList, Static


ASSETS_FOLDER_PATH = Path(__file__).parent.parent / "assets"

class SettingsScreen(ModalScreen[None]):
    language: str | None = None
    tag: list[str] | None = None

    CSS_PATH = ASSETS_FOLDER_PATH / "settings_screen.tcss"
    BINDINGS = [Binding("escape", "close", "Close", show=True)]

    def compose(self) -> ComposeResult:
        with ScrollableContainer(id="settings_screen_container"):
            yield Static("Settings", id="settings_screen_title")

            with Session() as session:
                language_items = self._get_items(session, LanguageService, "get_all_languages")
                tag_items = self._get_items(session, TagService, "get_all_tags")

                yield Select([(index, language) for index, language in language_items], prompt="Select language", allow_blank=False, id="settings_screen_language")
                yield SelectionList(*[(index, tag) for index, tag in tag_items], id="settings_screen_tags")

            yield Footer()

    def on_mount(self) -> None:
        self.query_one(Select).border_title = "Select language"
        self.query_one(SelectionList).border_title = "Select tags"

    def _get_items(self, session: Session, service_class, method_name: str) -> list[tuple[str, int]]:
        """Generic method to get items from a service."""
        service = service_class(session)
        items = getattr(service, method_name)()
        return [(item.name, item.name) for index, item in enumerate(items)]

    @on(SelectionList.SelectedChanged)
    def on_selection_changed(self, event: SelectionList.SelectedChanged) -> None:
        """Handle selection changes in the SelectionList."""
        self.refresh()

    @on(SelectionList.SelectionHighlighted)
    def on_selection_highlighted(self, event: SelectionList.SelectionHighlighted) -> None:
        """Handle selection highlighting in the SelectionList."""
        self.refresh()

    def action_close(self) -> None:
        """Close the screen."""
        self.language = self.query_one("#settings_screen_language", Select).value
        self.tag = self.query_one("#settings_screen_tags", SelectionList).selected
        self.app.pop_screen()
