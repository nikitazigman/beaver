import pytest

from algorithms.dynamic_programming.subset_sum.main import can_sum


@pytest.mark.parametrize(
    "target_sum, numbers, expected",
    (
        (7, [2, 3], True),
        (7, [5, 3, 4, 7], True),
        (7, [2, 4], False),
        (8, [2, 3, 5], True),
        (300, [7, 14], False),
    ),
)
def test_can_sum(target_sum: int, numbers: list[int], expected: bool):
    assert can_sum(target_sum, numbers) == expected
