from pathlib import Path

import pytest

from beaver_etl.project_parsers.python_project_parsers import (
    PoetryProjectParser,
)


TEST_SOURCE_PATH = Path(__file__).parent.parent / "source"


@pytest.mark.parametrize(
    "path_to_project, expected_attributes",
    (
        (
            TEST_SOURCE_PATH / "test_project",
            {
                "source_code": (
                    TEST_SOURCE_PATH / "test_project/src/main.py"
                ).read_text(),
                "readme": (
                    TEST_SOURCE_PATH / "test_project/README.md"
                ).read_text(),
                "link_to_task": "https://leetcode.com/problems/merge-sorted-array/",
                "language": "python",
                "title": "Merge Sorted Array",
                "types": ["array", "two pointers", "sorting"],
            },
        ),
    ),
)
def test_poetry_project_parser(
    path_to_project: Path, expected_attributes: dict
):
    poetry_project_parser = PoetryProjectParser()
    code_document = poetry_project_parser.retrieve_data(path_to_project)

    assert code_document.model_dump() == expected_attributes
