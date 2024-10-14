import math


def hash1(key, size):
    return key % size


def hash2(constant):
    def inner(key, size):
        return int(size * math.modf(key * constant)[0])

    return inner


def hash3(key, size):
    return int(size * math.modf(key * (math.sqrt(5) - 1) / 2)[0])


def double_hash(key, size, hash1, hash2, i=0):
    return (hash1(key, size) + i * hash2(key, size)) % size


class Entry:
    def __init__(self, key, value):
        self.key = key
        self.value = value


class HashMapAddressing:
    def __init__(self, capacity=53, get_hash=hash1):
        self.size = 0
        self.capacity = capacity
        self.get_hash = get_hash
        self.buckets = [None] * self.capacity

    def put(self, key, value):
        if self.capacity == self.size:
            self._reinit()
        self._put(key, value)

    def _put(self, key, value):
        index = self._find_place(key)
        self.buckets[index] = Entry(key, value)
        self.size += 1

    def get(self, key):
        index = self._find_place(key)
        if index is None:
            return None
        return self.buckets[index] and self.buckets[index].value

    def _hash(self, key, i=0):
        return double_hash(key, self.capacity, self.get_hash, hash3, i)

    def _find_place(self, key):
        for i in range(0, self.capacity):
            index = self._hash(key, i)
            if self.buckets[index] is None or self.buckets[index].key == key:
                return index
        return None

    def _reinit(self):
        self.capacity *= 2
        old_buckets = self.buckets
        self.buckets = [None] * self.capacity
        self.size = 0
        for entry in old_buckets:
            self._put(entry.key, entry.value)
