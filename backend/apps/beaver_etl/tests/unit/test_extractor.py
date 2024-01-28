from pathlib import Path

import pytest

from beaver_etl.extractors.schema import ExtractorCodeSchema


DATASET_PATH = Path(__file__).parent.parent / "data"


@pytest.mark.parametrize(
    "dataset_dir, expected",
    (
        (
            DATASET_PATH,
            [
                ExtractorCodeSchema(
                    source_code=(
                        DATASET_PATH
                        / "algorithms/Arrays/MergeSortedArray/src/main.py"
                    ).read_text(),
                    language="python",
                    link_to_task="https://leetcode.com/problems/merge-sorted-array/",
                    title="Merge Sorted Array",
                    types=["array", "two pointers", "sorting"],
                    readme=(
                        DATASET_PATH
                        / "algorithms/Arrays/MergeSortedArray/README.md"
                    ).read_text(),
                ),
                ExtractorCodeSchema(
                    source_code=(
                        DATASET_PATH.joinpath(
                            "algorithms/Arrays/RemoveDuplicatesFromSortedArrayII/src/main.py"
                        )
                    ).read_text(),
                    language="python",
                    link_to_task="https://leetcode.com/problems/remove-duplicates-from-sorted-array-ii/",
                    title="Remove Duplicates from Sorted Array II",
                    types=["array", "two pointers"],
                    readme=(
                        DATASET_PATH.joinpath(
                            "algorithms/Arrays/RemoveDuplicatesFromSortedArrayII/README.md"
                        )
                    ).read_text(),
                ),
                ExtractorCodeSchema(
                    source_code=(
                        DATASET_PATH.joinpath(
                            "algorithms/TwoPointers/ValidPalindrome/src/main.py"
                        )
                    ).read_text(),
                    language="python",
                    link_to_task="https://leetcode.com/problems/valid-palindrome/",
                    title="Valid Palindrome",
                    types=["two pointers", "string"],
                    readme=(
                        DATASET_PATH.joinpath(
                            "algorithms/TwoPointers/ValidPalindrome/README.md"
                        )
                    ).read_text(),
                ),
            ],
        ),
    ),
)
def test_extractor(dataset_dir: Path, expected: list[ExtractorCodeSchema]):
    raise NotImplementedError
