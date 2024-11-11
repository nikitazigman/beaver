from textual.containers import Center
from textual.screen import Screen
from textual.widgets import Button, Static


class ErrorMessage(Screen):
    def __init__(self, message: str):
        super().__init__()
        self.message = message

    def compose(self):
        yield Center(Static(f"Error: {self.message}"))
        yield Center(Button("Retry", id="retry"))
        yield Center(Button("Close", id="close"))

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "retry":
            self.app.pop_screen()
            self.app.action_load_new_game()
        elif event.button.id == "close":
            self.app.pop_screen()
