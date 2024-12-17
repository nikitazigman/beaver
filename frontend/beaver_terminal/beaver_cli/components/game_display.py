from beaver_cli.components.code import (
    Code,
    UserCompletedCode,
    UserCorrectEvent,
    UserErrorEvent,
    UserStartTyping,
)
from beaver_cli.components.info_label import InfoDisplay
from beaver_cli.components.link_to_code import LinkToCode
from beaver_cli.components.time_label import TimeDisplay
from beaver_cli.schemas.code_document import CodeDocument
from beaver_cli.schemas.statistic import Statistic
from textual import on
from textual.containers import Container
from textual.css.query import NoMatches


class GameDisplay(Container):
    DEFAULT_CSS = """
        GameDisplay {
            layout: vertical;
            background: $panel;
            align: center middle;
            padding: 1 2;
        }
        .info_container {
            height: auto;
        }
    """

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.statistic = Statistic(typing_errors=[], typing_events=[])

    def on_mount(self) -> None:
        ...

    @on(message_type=UserStartTyping)
    async def handle_start(self) -> None:
        time_display = TimeDisplay()
        try:
            self.query_one(selector="#info-language").remove()
            self.query_one(selector="#info-title").remove()
            self.query_one(selector="#info-tags").remove()
            await self.mount(time_display, before=self.query_one(selector=Code))
            time_display.start()
        except NoMatches:
            pass

    @on(message_type=UserCompletedCode)
    async def handle_stop(self) -> None:
        time_display: TimeDisplay = self.query_one(selector=TimeDisplay)
        time_display.stop()

    @on(message_type=UserErrorEvent)
    async def handle_typo(self) -> None:
        time_display: TimeDisplay = self.query_one(selector=TimeDisplay)
        self.statistic.typing_errors.append(time_display.time)

    @on(message_type=UserCorrectEvent)
    async def handle_correct(self) -> None:
        time_display: TimeDisplay = self.query_one(selector=TimeDisplay)
        self.statistic.typing_events.append(time_display.time)

    def get_game_statistic(self) -> Statistic:
        return self.statistic

    def load_new_game(self, code_document: CodeDocument) -> None:
        [widget.remove() for widget in self.query()]

        self.mount(
            LinkToCode(
                renderable=f"# Title: [@click=app.open_link('{code_document.link_to_project}')]{code_document.title}[/]",
                id="info-title",
            ),
            InfoDisplay(
                renderable=code_document.language,
                prefix="# Language:",
                id="info-language",
            ),
            InfoDisplay(
                renderable=str(code_document.tags),
                prefix="# Tags:",
                id="info-tags",
            ),
            Code(
                language=code_document.language,
                read_only=True,
                theme="vscode_dark",
                text=code_document.code,
                show_line_numbers=True,
                id="code",
            ),
        )
