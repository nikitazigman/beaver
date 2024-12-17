from pathlib import Path

from beaver_cli.schemas.language import Language
from beaver_cli.schemas.tags import Tag
from beaver_cli.services.api import BeaverAPIService
from textual import log
from textual.app import ComposeResult, on
from textual.binding import Binding
from textual.containers import ScrollableContainer
from textual.screen import ModalScreen
from textual.widgets import Footer, Select, SelectionList, Static


ASSETS_FOLDER_PATH: Path = Path(__file__).parent.parent / "assets"


class SettingsScreen(ModalScreen[None]):
    CSS_PATH: Path = ASSETS_FOLDER_PATH / "settings_screen.tcss"  # type: ignore
    BINDINGS: list[Binding] = [
        Binding(key="escape", action="save_close", description="Save", show=True),
    ]

    def __init__(self, beaver_api: BeaverAPIService) -> None:
        super().__init__()
        self.beaver_api: BeaverAPIService = beaver_api

    def compose(self) -> ComposeResult:
        with ScrollableContainer(id="settings_screen_container"):
            yield Static(renderable="Settings", id="settings_screen_title")

            language_items: list[Language] = self.beaver_api.get_all_languages()
            tag_items: list[Tag] = self.beaver_api.get_all_tags()

            yield Select[str](
                options=[(language.name, language.name) for language in language_items],
                prompt="Select language",
                allow_blank=False,
                id="settings_screen_language",
            )
            yield SelectionList[str](*[(tag.name, tag.name) for tag in tag_items], id="settings_screen_tags")

            yield Footer()

    def on_mount(self) -> None:
        self.query_one(Select).border_title = "Select language"
        self.query_one(SelectionList).border_title = "Select tags"

    @on(message_type=SelectionList.SelectedChanged)
    def on_selection_changed(self, event: SelectionList.SelectedChanged) -> None:
        """Handle selection changes in the SelectionList."""
        self.refresh()

    @on(message_type=SelectionList.SelectionHighlighted)
    def on_selection_highlighted(self, event: SelectionList.SelectionHighlighted) -> None:
        """Handle selection highlighting in the SelectionList."""
        self.refresh()

    def action_save_close(self) -> None:
        """Close the screen."""
        language_selector: Select[str] = self.query_one(selector="#settings_screen_language", expect_type=Select)
        tags_selector: SelectionList[str] = self.query_one(selector="#settings_screen_tags", expect_type=SelectionList)
        language: str | None = language_selector.value  # type: ignore
        tags: list[str] = tags_selector.selected
        log.info(f"user selected: {language=}, tags={tags}")
        self.beaver_api.set_settings(tags=tags, language=language)

        self.app.pop_screen()
