from pathlib import Path

import pytest

from beaver_etl.parsers import ParserCodeSchema, PoetryProjectParser


PROJECTS_DIR = (
    Path(__file__).parent.parent.parent.parent
    / "algorithms"
    / "classic_algorithms"
)


@pytest.fixture(scope="module")
def parser() -> PoetryProjectParser:
    return PoetryProjectParser(
        path_to_main="src/main.py",
        path_to_pyproject_toml="pyproject.toml",
        path_to_readme="README.md",
    )


def test_project_structure(parser: PoetryProjectParser) -> None:
    for project in PROJECTS_DIR.iterdir():
        if project.is_dir():
            assert (
                project / "src/main.py"
            ).exists(), f"{project} is missing src/main.py"
            assert (
                project / "pyproject.toml"
            ).exists(), f"{project} is missing pyproject.toml"
            assert (
                project / "README.md"
            ).exists(), f"{project} is missing README.md"

            try:
                parsed_schema: ParserCodeSchema = parser.parse(project)
                assert parsed_schema.code, "Parsed source code is empty"
                assert (
                    parsed_schema.link_to_project
                ), "Parsed link to project is empty"
                assert parsed_schema.title, "Parsed title is empty"
                assert parsed_schema.tags, "Parsed tags are empty"
            except Exception as e:
                pytest.fail(f"Failed to parse project {project}: {e}")
