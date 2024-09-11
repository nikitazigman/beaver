import pytest

from src.main import LruDict


@pytest.fixture
def sample_lru():
    return LruDict(maxsize=3)


def test_add_and_get(sample_lru):
    sample_lru.add(1, "one")
    assert sample_lru.get(1) == "one"


def test_update_value(sample_lru):
    sample_lru.add(1, "one")
    sample_lru.add(1, "uno")
    assert sample_lru.get(1) == "uno"


def test_get_nonexistent_key(sample_lru):
    assert sample_lru.get(999) is None


def test_remove_old(sample_lru):
    sample_lru.add(1, "one")
    sample_lru.add(2, "two")
    sample_lru.add(3, "three")
    sample_lru.add(4, "four")  # This should evict key 1
    assert sample_lru.get(1) is None
    assert sample_lru.get(2) == "two"
    assert sample_lru.get(3) == "three"
    assert sample_lru.get(4) == "four"


def test_lru_order(sample_lru):
    sample_lru.add(1, "one")
    sample_lru.add(2, "two")
    sample_lru.add(3, "three")
    sample_lru.get(1)  # Access key 1 to make it most recently used
    sample_lru.add(4, "four")  # This should evict key 2
    assert sample_lru.get(2) is None
    assert sample_lru.get(1) == "one"
    assert sample_lru.get(3) == "three"
    assert sample_lru.get(4) == "four"
