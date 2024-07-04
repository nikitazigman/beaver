from beaver_cli.components.footer import BeaverFooter
from beaver_cli.components.game_display import GameDisplay
from beaver_cli.components.header import BeaverHeader

from textual.app import App, ComposeResult


code = "def sum(a: int, b: int):\n    return a + b\n"


class BeaverCli(App):
    CSS_PATH = "main.tcss"

    BINDINGS = [
        # Binding("d", "toggle_dark", "Toggle dark mode", show=True),
    ]

    def compose(self) -> ComposeResult:
        yield BeaverHeader(name="Beaver CLI")
        yield GameDisplay()
        yield BeaverFooter()


if __name__ == "__main__":
    app = BeaverCli()
    app.run()
