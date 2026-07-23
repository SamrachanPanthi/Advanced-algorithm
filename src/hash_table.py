"""Hash table with separate chaining for fast city lookup by name.

Doubles the bucket count once the load factor passes 0.75, which is what
keeps chains short and lookups close to O(1) as the table grows.
"""


class HashTableChaining:
    def __init__(self, initial_capacity=16, load_factor_threshold=0.75):
        self._capacity = initial_capacity
        self._threshold = load_factor_threshold
        self._buckets = [[] for _ in range(self._capacity)]
        self._size = 0

    def __len__(self):
        return self._size

    def _index(self, key):
        return hash(key) % self._capacity

    def _resize(self):
        old_buckets = self._buckets
        self._capacity *= 2
        self._buckets = [[] for _ in range(self._capacity)]
        for bucket in old_buckets:
            for k, v in bucket:
                self._buckets[self._index(k)].append((k, v))

    def insert(self, key, value):
        bucket = self._buckets[self._index(key)]
        for i, (k, _) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return
        bucket.append((key, value))
        self._size += 1
        if self._size / self._capacity > self._threshold:
            self._resize()

    def search(self, key):
        for k, v in self._buckets[self._index(key)]:
            if k == key:
                return v
        return None

    def delete(self, key):
        bucket = self._buckets[self._index(key)]
        for i, (k, _) in enumerate(bucket):
            if k == key:
                bucket.pop(i)
                self._size -= 1
                return True
        return False

    def load_factor(self):
        return self._size / self._capacity

    def max_chain_length(self):
        return max((len(b) for b in self._buckets), default=0)
