from abc import ABC, abstractmethod
from pathlib import Path

from src.schemas import InfoCodeSchema, ParserCodeSchema


class IParser(ABC):
    @abstractmethod
    def parse(self, project: Path) -> ParserCodeSchema:
        """retrieves data from a python project"""


class ProjectParser(IParser):
    def __init__(self, beaver_file: str, path_to_dataset: Path) -> None:
        self.beaver_file: str = beaver_file
        self.path_to_dataset: Path = path_to_dataset

    def parse(self, project: Path) -> ParserCodeSchema:
        code_info_json: str = project.joinpath(self.beaver_file).read_text()
        code_info: InfoCodeSchema = InfoCodeSchema.model_validate_json(
            json_data=code_info_json
        )
        code: str = self.path_to_dataset.joinpath(code_info.path).read_text()

        return ParserCodeSchema(
            title=code_info.title,
            code=code,
            link_to_project=code_info.link_to_project,
            language=code_info.language,
            tags=code_info.tags,
            contributors=code_info.contributors,
        )


def get_parser(beaver_file: str, path_to_dataset: Path) -> IParser:
    return ProjectParser(
        beaver_file=beaver_file,
        path_to_dataset=path_to_dataset,
    )
