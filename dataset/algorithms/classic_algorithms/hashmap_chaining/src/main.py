import random

from collections import deque, reduce


def hash(key, size):
    return key % size


class Entry:
    def __init__(self, key, value):
        self.key = key
        self.value = value


class HashMapChains:
    def __init__(self, capacity=53, get_hash=hash):
        self.size = 0
        self.capacity = capacity
        self.get_hash = get_hash
        self.buckets = [deque() for _ in range(self.capacity)]

    def put(self, key, value):
        index = self.get_hash(key, self.capacity)
        bucket = self.buckets[index]
        founded_entry = next(
            (entry for entry in bucket if entry.key == key), None
        )
        if founded_entry is not None:
            founded_entry.value = value
        else:
            bucket.append(Entry(key, value))
            self.size += 1

    def get(self, key):
        index = self.get_hash(key, self.capacity)
        bucket = self.buckets[index]
        return next(
            (entry.value for entry in bucket if entry.key == key), None
        )

    def get_size(self):
        return self.size


def get_metrics(
    hash_fn, size=30007, keys_size=37000, random_range=50000, value=5
):
    map = HashMapChains(size, hash_fn)
    for i in range(keys_size):
        random_key = random.randint(1, random_range)
        map.put(random_key, value)
    return {
        "average-chain-length": get_average_chain_length(map),
        "medium-chain-length": get_medium_chain_length(map),
        "max-chain-length": get_max_chain_length(map),
    }


def get_average_chain_length(map):
    buckets = map.buckets
    elements = 0
    count = 0
    for bucket in buckets:
        elements += len(bucket)
        if len(bucket) > 0:
            count += 1
    return elements / count


def get_medium_chain_length(map):
    buckets = list(filter(lambda bucket: len(bucket) > 0, map.buckets))
    buckets.sort(key=lambda bucket: len(bucket))
    return len(buckets[len(buckets) // 2])


def get_max_chain_length(map):
    return reduce(
        lambda max_chain, bucket: max(max_chain, len(bucket)), map.buckets, 0
    )
