import pytest

from src.main import Solution


@pytest.mark.parametrize(
    "s, expected",
    (
        ("A man, a plan, a canal: Panama", True),
        ("race a car", False),
        (" ", True),
    ),
)
def test_main(s, expected: list[int]):
    result = Solution().isPalindrome(s)
    assert result == expected
