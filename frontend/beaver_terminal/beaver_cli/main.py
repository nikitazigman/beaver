from beaver_cli.components.footer import BeaverFooter
from beaver_cli.components.game_display import GameDisplay
from beaver_cli.components.header import BeaverHeader

from textual.app import App, ComposeResult
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
    ]

    def compose(self) -> ComposeResult:
        yield BeaverHeader(name="Beaver CLI")
        yield GameDisplay()
        yield BeaverFooter()

    def action_load_new_game(self) -> None:
        game_display = self.query_one(GameDisplay)
        game_display.load_new_game()
        game_display.focus()


if __name__ == "__main__":
    app = BeaverCli()
    app.run()
