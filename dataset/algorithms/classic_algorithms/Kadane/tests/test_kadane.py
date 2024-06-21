import pytest

from algorithms.classic_algorithms.kadane.src.main import kadane


@pytest.mark.parametrize(
    "array, expected",
    (
        ([1, 2, 3, 4, 5], 15),
        ([-2, -3, 4, -1, -2, 1, 5, -3], 7),
        ([-1, -2, -3, -4], -1),
        ([10], 10),
        ([0, 0, 0, 0], 0),
    ),
)
def test_kadane(array: list[int], expected: int):
    assert kadane(array) == expected
