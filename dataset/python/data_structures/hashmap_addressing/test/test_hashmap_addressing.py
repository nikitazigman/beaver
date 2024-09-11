import pytest

from src.main import HashMapAddressing


@pytest.fixture
def sample_hash_map():
    return HashMapAddressing()


def test_put_and_get(sample_hash_map):
    sample_hash_map.put(1, "one")
    assert sample_hash_map.get(1) == "one"


def test_update_value(sample_hash_map):
    sample_hash_map.put(1, "one")
    sample_hash_map.put(1, "uno")
    assert sample_hash_map.get(1) == "uno"


def test_get_nonexistent_key(sample_hash_map):
    assert sample_hash_map.get(999) is None


def test_reinit():
    hash_map = HashMapAddressing(capacity=2)
    hash_map.put(1, "one")
    hash_map.put(2, "two")
    hash_map.put(3, "three")
    assert hash_map.get(1) == "one"
    assert hash_map.get(2) == "two"
    assert hash_map.get(3) == "three"
