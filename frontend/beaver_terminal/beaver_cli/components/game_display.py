from beaver_cli.components.code import Code
from beaver_cli.components.tag_display import TagDisplay
from beaver_cli.components.time_display import TimeDisplay
from beaver_cli.services.code_document import CodeService
from beaver_cli.utils.session import Session
from textual.containers import Horizontal
from textual.widgets import Static


class GameDisplay(Static):
    DEFAULT_CSS = """
        GameDisplay {
            layout: vertical;
            background: $boost;
            # margin: 1;
            # min-width: 50;
            padding: 0;
        }
        .tag_display {
            layout: horizontal;
            background: $background;
            padding: 0;
            height: auto;
        }
    """

    def on_mount(self) -> None:
        self.load_new_game()

    def load_new_game(self) -> None:
        with Session() as session:
            code_document = CodeService(session).get_code_document()

        tag_widgets = [
            TagDisplay(tag, id=f"tag{i}")
            for i, tag in enumerate(code_document.tags)
        ]
        code_widget = Code(
            language=code_document.language,
            read_only=True,
            text=code_document.code,
        )

        self.mount(
            TimeDisplay(),
            Horizontal(*tag_widgets, id="tag_display", classes="tag_display"),
            code_widget,
        )
