import pytest

from algorithms.substring_search.bm_search.main import boyer_moore_search


@pytest.mark.parametrize(
    ["text", "pattern", "expected"],
    [
        pytest.param("HERE IS A SIMPLE EXAMPLE", "IS", 5, id="exists"),
        pytest.param("HERE IS A ", "NOTFOUND", None, id="does not exists"),
        pytest.param("HERE IS A SIMPLE EXAMPLE", "HERE", 0, id="at start"),
        pytest.param("HERE IS A SIMPLE EXAMPLE", "EXAMPLE", 17, id="at end"),
    ],
)
def test_bm_search(text: str, pattern: str, expected: int) -> None:
    assert boyer_moore_search(text=text, pattern=pattern) == expected
