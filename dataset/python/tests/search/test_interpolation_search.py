import pytest

from algorithms.search.interpolation_search.main import interpolation_search


@pytest.mark.parametrize(
    ["array", "element", "expected"],
    [
        pytest.param([10, 20, 30, 40, 50], 30, 2, id="exists"),
        pytest.param([10, 20, 30, 40, 50], 60, None, id="does not exists"),
        pytest.param([], 30, None, id="empty array"),
        pytest.param([10, 20, 30, 40, 50], 10, 0, id="first element"),
        pytest.param([10, 20, 30, 40, 50], 50, 4, id="last element"),
    ],
)
def test_interpolation_search(
    array: list[int], element: int, expected: int | None
) -> None:
    assert interpolation_search(array=array, element=element) == expected
