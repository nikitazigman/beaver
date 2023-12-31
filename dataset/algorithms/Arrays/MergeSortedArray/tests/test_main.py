import pytest

from src.main import Solution


@pytest.mark.parametrize(
    "nums1, m, nums2, n, expected",
    (
        ([1, 2, 3, 0, 0, 0], 3, [2, 5, 6], 3, [1, 2, 2, 3, 5, 6]),
        ([1], 1, [], 0, [1]),
        ([], 0, [1], 1, [1]),
    ),
)
def test_main(
    nums1: list[int], m: int, nums2: list[int], n: int, expected: list[int]
):
    Solution().merge(nums1, m, nums2, n)
    assert nums1 == expected
