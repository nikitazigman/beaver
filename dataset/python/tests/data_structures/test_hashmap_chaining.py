import random

from algorithms.data_structures.hashmap_chaining.main import (
    HashMapChains,
    get_average_chain_length,
    get_max_chain_length,
    get_medium_chain_length,
    get_metrics,
    hash,
)


def test_put_and_get():
    map = HashMapChains()
    map.put(1, "value1")
    assert map.get(1) == "value1"
    assert map.get(2) is None

    map.put(1, "value2")
    assert map.get(1) == "value2"

    map.put(2, "value3")
    assert map.get(2) == "value3"
    assert map.get_size() == 2


def test_get_size():
    map = HashMapChains()
    assert map.get_size() == 0

    map.put(1, "value1")
    assert map.get_size() == 1

    map.put(2, "value2")
    assert map.get_size() == 2

    map.put(1, "value3")
    assert map.get_size() == 2


def test_get_metrics():
    random.seed(0)
    metrics = get_metrics(hash)
    assert "average-chain-length" in metrics
    assert "medium-chain-length" in metrics
    assert "max-chain-length" in metrics

    assert metrics["average-chain-length"] > 0
    assert metrics["medium-chain-length"] > 0
    assert metrics["max-chain-length"] > 0


def test_get_average_chain_length():
    map = HashMapChains()
    map.put(1, "value1")
    map.put(2, "value2")
    map.put(1, "value3")  # Same key, should not increase size

    avg_chain_length = get_average_chain_length(map)
    assert avg_chain_length == 1.0


def test_get_medium_chain_length():
    map = HashMapChains()
    map.put(1, "value1")
    map.put(2, "value2")
    map.put(3, "value3")

    median_chain_length = get_medium_chain_length(map)
    assert median_chain_length == 1


def test_get_max_chain_length():
    map = HashMapChains()
    map.put(1, "value1")
    map.put(2, "value2")
    map.put(1, "value3")

    max_chain_length = get_max_chain_length(map)
    assert max_chain_length == 1
