from beaver_cli.components.code import (
    Code,
    UserCompletedCode,
)
from beaver_cli.components.footer import BeaverFooter
from beaver_cli.components.game_display import GameDisplay
from beaver_cli.components.header import BeaverHeader
from beaver_cli.components.help_screen import HelpScreen
from beaver_cli.components.result_display import ResultDisplay
from beaver_cli.components.settings_screen import SettingsScreen

from textual import on
from textual.app import App, ComposeResult, NoMatches
from textual.binding import Binding


code = "def sum(a: int, b: int):\n    return a + b\n"


class BeaverCli(App):
    CSS_PATH = "main.tcss"

    BINDINGS = [
        Binding("ctrl+c", "quit", "Quit", show=True, priority=True),
        Binding(
            "ctrl+n",
            "load_new_game",
            "Next",
            show=True,
            priority=True,
        ),
        Binding(
            "ctrl+d",
            "toggle_dark",
            "Toggle dark mode",
            show=True,
        ),
        Binding(
            "f1",
            "show_help",
            "Show help",
            show=True,
        ),
        Binding(
            "f2",
            "show_settings",
            "Show settings",
            show=True,
        ),
    ]

    SCREENS = {"settings": SettingsScreen()}

    def compose(self) -> ComposeResult:
        yield BeaverHeader(name="Beaver CLI")
        yield GameDisplay()
        yield BeaverFooter()

    @on(UserCompletedCode)
    def show_statistics(self, event: UserCompletedCode) -> None:
        game_display = self.query_one(GameDisplay)
        statistic = game_display.get_game_statistic()
        game_display.remove()

        self.mount(
            ResultDisplay(
                statistic=statistic,
                intervals=20,
            )
        )

    def action_load_new_game(self) -> None:
        try:
            self.query_one(ResultDisplay).remove()
        except NoMatches:
            ...

        try:
            game_display = self.query_one(GameDisplay)
            settings: SettingsScreen = self.SCREENS["settings"]
            language, tag = settings.language, settings.tag

            game_display.load_new_game(language, tag)
            game_display.focus()
        except NoMatches:
            self.mount(GameDisplay())

    def action_toggle_dark(self) -> None:
        super().action_toggle_dark()
        code_widget: Code = self.query_one("#code")
        code_widget.theme = "vscode_dark" if self.dark else "github_light"

    def action_show_help(self) -> None:
        self.push_screen(HelpScreen())

    def action_show_settings(self) -> None:
        self.push_screen("settings")


def main() -> None:
    app = BeaverCli()
    app.run()


if __name__ == "__main__":
    main()
