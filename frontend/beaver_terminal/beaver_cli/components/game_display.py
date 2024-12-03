from beaver_cli.components.code import (
    Code,
    UserCompletedCode,
    UserCorrectEvent,
    UserErrorEvent,
    UserStartTyping,
)
from beaver_cli.components.error_message import ErrorMessage
from beaver_cli.components.info_label import InfoDisplay
from beaver_cli.components.link_to_code import LinkToCode
from beaver_cli.components.time_label import TimeDisplay
from beaver_cli.schemas.code_document import CodeDocument
from beaver_cli.schemas.statistic import Statistic
from beaver_cli.services.code_document import CodeService
from beaver_cli.utils.session import Session
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

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.statistic = Statistic(typing_errors=[], typing_events=[])

    def on_mount(self) -> None:
        self.load_new_game()

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

    @on(UserCompletedCode)
    async def handle_stop(self) -> None:
        time_display: TimeDisplay = self.query_one(selector=TimeDisplay)
        time_display.stop()

    @on(UserErrorEvent)
    async def handle_typo(self) -> None:
        time_display: TimeDisplay = self.query_one(selector=TimeDisplay)
        self.statistic.typing_errors.append(time_display.time)

    @on(UserCorrectEvent)
    async def handle_correct(self) -> None:
        time_display: TimeDisplay = self.query_one(selector=TimeDisplay)
        self.statistic.typing_events.append(time_display.time)

    def get_game_statistic(self) -> Statistic:
        return self.statistic

    def fetch_code_document(self, language: str | None = None, tags: list[str] | None = None) -> CodeDocument | None:
        try:
            with Session() as session:
                return CodeService(session=session).get_code_document(language=language, tags=tags)
        except Exception as e:
            [widget.remove() for widget in self.query()]
            self.mount(ErrorMessage(str(e)))
            return None

    def load_new_game(self, language: str | None = None, tags: list[str] | None = None) -> None:
        code_document: CodeDocument | None = self.fetch_code_document(language=language, tags=tags)

        if code_document is None:
            return

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
