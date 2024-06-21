import pytest

from algorithms.classic_algorithms.SubarraySum.src.main import Solution


@pytest.mark.parametrize(
    "arr, target, expected",
    [
        ([1, 2, 3, 4, 5], 9, True),
        ([1, 2, 3, 4, 5], 15, True),
        ([1, 2, 3, 7, 5], 10, True),
        ([1, 2, 3, 4, 5], 21, False),
        ([], 0, False),
    ]
)
def test_is_subsum_exist(arr: list[int], target: int, expected: bool):
    assert Solution().is_subsum_exist(arr, target) == expected
