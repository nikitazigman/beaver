from pathlib import Path

from textual.app import ComposeResult
from textual.containers import Center
from textual.screen import Screen
from textual.widgets import Button, Static


ASSETS_FOLDER_PATH = Path(__file__).parent.parent / "assets"


class ErrorMessage(Screen):
    CSS_PATH = ASSETS_FOLDER_PATH /  "error_screen.tcss"

    def __init__(self, message: str):
        super().__init__()
        self.message = message

    def compose(self) -> ComposeResult:
        yield Static(f"Error: {self.message}", id="message")
        yield Center(Button("Retry", id="retry"))
        yield Center(Button("Close", id="close"))

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "retry":
            self.app.pop_screen()
            self.app.action_load_new_game()
        elif event.button.id == "close":
            self.app.pop_screen()
