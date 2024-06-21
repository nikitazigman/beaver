import pytest

from algorithms.Arrays.RemoveDuplicatesFromSortedArrayII.src.main import (
    Solution,
)


@pytest.mark.parametrize(
    "nums, expected",
    (
        ([1, 1, 1, 2, 2, 3], [1, 1, 2, 2, 3]),
        ([0, 0, 1, 1, 1, 1, 2, 3, 3], [0, 0, 1, 1, 2, 3, 3]),
    ),
)
def test_main(nums: list[int], expected: list[int]):
    array_length = Solution().removeDuplicates(nums)
    assert nums[:array_length] == expected
