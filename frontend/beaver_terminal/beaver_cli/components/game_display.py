from collections.abc import Generator

from beaver_cli.components.code import (
    Code,
    UserCompletedCode,
    UserCorrectEvent,
    UserErrorEvent,
    UserStartTyping,
)
from beaver_cli.components.info_label import InfoDisplay
from beaver_cli.components.time_label import TimeDisplay
from beaver_cli.schemas.statistic import Statistic
from beaver_cli.services.code_document import CodeService
from beaver_cli.utils.session import Session
from textual import on
from textual.app import NoMatches
from textual.containers import Container


class GameDisplay(Container):
    DEFAULT_CSS = """
        GameDisplay {
            layout: vertical;
            background: $panel;
            # border: tall $accent;
            align: center middle;
            # margin: 1;
            # min-width: 50;
            padding: 1 2;
        }
        .info_container {
            height: auto;
        }
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.statistic = Statistic(typing_errors=[], typing_events=[])

    def on_mount(self) -> Generator[None, None, None]:
        self.load_new_game()

    @on(UserStartTyping)
    async def handle_start(self) -> None:
        time_display = TimeDisplay()
        try:
            self.query_one("#info-language").remove()
            self.query_one("#info-title").remove()
            self.query_one("#info-tags").remove()
            await self.mount(time_display, before=self.query_one(Code))
            time_display.start()
        except NoMatches:
            pass

    @on(UserCompletedCode)
    async def handle_stop(self) -> None:
        time_display = self.query_one(TimeDisplay)
        time_display.stop()

    @on(UserErrorEvent)
    async def handle_typo(self) -> None:
        time_display = self.query_one(TimeDisplay)
        self.statistic.typing_errors.append(time_display.time)

    @on(UserCorrectEvent)
    async def handle_correct(self) -> None:
        time_display = self.query_one(TimeDisplay)
        self.statistic.typing_events.append(time_display.time)

    def get_game_statistic(self) -> Statistic:
        return self.statistic

    def load_new_game(self, language: str = None, tags: list[str] = None) -> None:
        with Session() as session:
            code_document = CodeService(session).get_code_document(language=language, tags=tags)

        [widget.remove() for widget in self.query()]

        self.mount(
            InfoDisplay(
                code_document.language,
                prefix="# Language:",
                id="info-language",
            ),
            InfoDisplay(
                code_document.title,
                prefix="# Title:",
                id="info-title",
            ),
            InfoDisplay(
                str(code_document.tags), prefix="# Tags:", id="info-tags"
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
