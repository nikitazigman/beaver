import pytest

from algorithms.search.linear_search.main import linear_search


@pytest.mark.parametrize(
    ["array", "element", "expected"],
    [
        pytest.param([10, 20, 30, 40, 50], 30, 2, id="element exist"),
        pytest.param([10, 20, 30, 40], 60, None, id="element does not exist"),
        pytest.param([], 10, None, id="empty array"),
        pytest.param([10, 20, 30, 40, 50], 10, 0, id="first element"),
        pytest.param([10, 20, 30, 40, 50], 50, 4, id="last element"),
    ],
)
def test_linear_search(array: list[int], element: int, expected: int | None) -> None:
    assert linear_search(array=array, element=element) == expected
