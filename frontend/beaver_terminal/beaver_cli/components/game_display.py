from beaver_cli.components.code import Code
from beaver_cli.components.language_display import LanguageDisplay
from beaver_cli.components.tag_display import TagDisplay
from beaver_cli.components.time_display import TimeDisplay
from beaver_cli.services.code_document import CodeService
from beaver_cli.utils.session import Session
from textual import on
from textual.widgets import Static


class GameDisplay(Static):
    DEFAULT_CSS = """
        GameDisplay {
            layout: vertical;
            background: $panel;
            border: tall $accent;
            # margin: 1;
            # min-width: 50;
            padding: 0 2;
        }
        .info_container {
            height: auto;
        }
    """

    def on_mount(self) -> None:
        self.load_new_game()

    @on(Code.Running)
    async def handle_code_message(self, event: Code.Running) -> None:
        mapping = {
            True: self.handle_start,
            False: self.handle_stop,
        }
        await mapping[event.running]()

    async def handle_start(self) -> None:
        time_display = TimeDisplay()
        self.query_one(TagDisplay).remove()
        self.query_one(LanguageDisplay).remove()
        await self.mount(time_display, before=self.query_one(Code))
        time_display.start()

    def handle_stop(self) -> None:
        time_display = self.query_one(TimeDisplay)
        time_display.stop()

    def load_new_game(self) -> None:
        [widget.remove() for widget in self.query()]

        with Session() as session:
            code_document = CodeService(session).get_code_document()

        self.mount(
            LanguageDisplay(code_document.language, id="language"),
            TagDisplay(str(code_document.tags), id="tags"),
            Code(
                language=code_document.language,
                read_only=True,
                text=code_document.code,
                show_line_numbers=True,
            ),
        )
