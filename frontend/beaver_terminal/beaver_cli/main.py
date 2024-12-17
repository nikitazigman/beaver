import webbrowser

from contextlib import suppress
from queue import Empty, Queue

from beaver_cli.components.code import (
    Code,
    UserCompletedCode,
)
from beaver_cli.components.error_message import ErrorMessage
from beaver_cli.components.error_screen import ErrorScreen
from beaver_cli.components.footer import BeaverFooter
from beaver_cli.components.game_display import GameDisplay
from beaver_cli.components.header import BeaverHeader
from beaver_cli.components.help_screen import HelpScreen
from beaver_cli.components.result_display import ResultDisplay
from beaver_cli.components.settings_screen import SettingsScreen
from beaver_cli.schemas.code_document import CodeDocument
from beaver_cli.schemas.statistic import Statistic
from beaver_cli.services.api import BeaverAPIService

from textual import on
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.css.query import NoMatches


class BeaverCli(App):
    CSS_PATH = "main.tcss"

    BINDINGS: list[Binding] = [  # type: ignore
        Binding(key="ctrl+c", action="quit", description="Quit", show=True, priority=True),
        Binding(
            key="ctrl+n",
            action="load_new_game",
            description="Next",
            show=True,
            priority=True,
        ),
        Binding(
            key="ctrl+d",
            action="toggle_dark",
            description="Toggle dark mode",
            show=True,
        ),
        Binding(
            key="f1",
            action="show_help",
            description="Show help",
            show=True,
        ),
        Binding(
            key="f2",
            action="show_settings",
            description="Show settings",
            show=True,
        ),
    ]

    def __init__(self, beaver_api: BeaverAPIService, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.beaver_api: BeaverAPIService = beaver_api

    def compose(self) -> ComposeResult:
        yield BeaverHeader(name="Beaver CLI")

        game_display = GameDisplay()
        self.mount(game_display)

        if (code_document := self.beaver_api.get_code_document()) is not None:
            game_display.load_new_game(code_document=code_document)

        yield BeaverFooter()

    @on(message_type=UserCompletedCode)
    def show_statistics(self, event: UserCompletedCode) -> None:
        game_display: GameDisplay = self.query_one(selector=GameDisplay)
        statistic: Statistic = game_display.get_game_statistic()
        game_display.remove()

        self.mount(ResultDisplay(statistic=statistic, intervals=20))

    def action_load_new_game(self) -> None:
        with suppress(NoMatches):
            self.query_one(selector=ResultDisplay).remove()
        with suppress(NoMatches):
            self.query_one(selector=ErrorMessage).remove()

        if len(self.screen_stack) > 1:
            self.pop_screen()

        try:
            game_display: GameDisplay = self.query_one(selector=GameDisplay)
            code_document: CodeDocument | None = self.beaver_api.get_code_document()

            if code_document is None:
                self.beaver_api.set_settings(tags=[], language=None)
                self.push_screen(
                    screen=ErrorScreen(
                        error_message="The requested code document could not be found. "
                        "Please try a different combination of tags or language, "
                        "as the specified document may not yet exist in the database."
                    )
                )

            else:
                game_display.load_new_game(code_document=code_document)
                game_display.focus()
                return

        except NoMatches:
            self.mount(GameDisplay())

        except Empty as e:
            self.push_screen(
                screen=ErrorScreen(error_message=f"An unexpected error occurred while fetching the code document: {e}")
            )

        self.beaver_api.set_settings(tags=[], language=None)

    def action_toggle_dark(self) -> None:
        super().action_toggle_dark()
        code_widget: Code = self.query_one(selector="#code")  # type: ignore
        code_widget.theme = "vscode_dark" if self.dark else "github_light"

    def action_show_help(self) -> None:
        self.push_screen(screen=HelpScreen())

    def action_show_settings(self) -> None:
        self.push_screen(screen=SettingsScreen(beaver_api=self.beaver_api))

    def action_open_link(self, link_to_code: str) -> None:
        webbrowser.open(url=link_to_code)


def main() -> None:
    queue = Queue(maxsize=5)
    with BeaverAPIService(queue=queue) as beaver_api:
        app = BeaverCli(beaver_api=beaver_api)
        app.run()


if __name__ == "__main__":
    main()
