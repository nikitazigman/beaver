from pathlib import Path

import pytest

from beaver_etl.extractors.project_parsers.python_project_parsers import (
    PoetryProjectParser,
)


TEST_PROJECT_PATH = (
    Path(__file__).parent.parent / "data/algorithms/Arrays/MergeSortedArray"
)


@pytest.mark.parametrize(
    "path_to_project, expected_attributes",
    (
        (
            TEST_PROJECT_PATH,
            {
                "source_code": (TEST_PROJECT_PATH / "src/main.py").read_text(),
                "readme": (TEST_PROJECT_PATH / "README.md").read_text(),
                "link_to_task": "https://leetcode.com/problems/merge-sorted-array/",
                "language": "python",
                "title": "Merge Sorted Array",
                "types": {"array", "two pointers", "sorting"},
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
