import pytest

from algorithms.substring_search.naive_search.main import naive_search


@pytest.mark.parametrize(
    ["text", "pattern", "expected"],
    [
        pytest.param("ABABDABACDABABCABAB", "ABABCABAB", 10, id="exist"),
        pytest.param("ABABDABACDABA", "ABCDEF", None, id="does not exist"),
        pytest.param("ABABCABAB", "ABAB", 0, id="at start"),
        pytest.param("ABABDABACDABABCABAB", "CABAB", 14, id="at end"),
        pytest.param("ABABDAB", "D", 4, id="single character"),
        pytest.param("ABABCABAB", "ABABCABAB", 0, id="the same text"),
    ],
)
def test_naive_search(text: str, pattern: str, expected: int | None) -> None:
    assert naive_search(text=text, pattern=pattern) == expected
