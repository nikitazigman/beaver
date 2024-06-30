from beaver_cli.components.code.code import Code
from beaver_cli.components.footer.footer import BeaverFooter
from beaver_cli.components.header.header import BeaverHeader

from textual.app import App, ComposeResult


class BeaverCli(App):
    CSS_PATH = "main.tcss"

    def compose(self) -> ComposeResult:
        yield BeaverHeader(name="Beaver CLI")
        yield Code()
        yield BeaverFooter()


if __name__ == "__main__":
    app = BeaverCli()
    app.run()
