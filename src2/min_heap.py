
class MinHeap:
    def __init__(self):
        self._data = []  # list of (priority, value)

    def __len__(self):
        return len(self._data)

    def is_empty(self):
        return not self._data

    def push(self, priority, value):
        self._data.append((priority, value))
        self._sift_up(len(self._data) - 1)

    def pop(self):
        if not self._data:
            raise IndexError("pop from empty heap")
        top = self._data[0]
        last = self._data.pop()
        if self._data:
            self._data[0] = last
            self._sift_down(0)
        return top

    def peek(self):
        if not self._data:
            raise IndexError("peek from empty heap")
        return self._data[0]

    @classmethod
    def build_heap(cls, items):
        """Build a heap from a list of (priority, value) in O(n)."""
        heap = cls()
        heap._data = list(items)
        n = len(heap._data)
        for i in range(n // 2 - 1, -1, -1):
            heap._sift_down(i)
        return heap

    def _sift_up(self, i):
        data = self._data
        while i > 0:
            parent = (i - 1) // 2
            if data[i][0] < data[parent][0]:
                data[i], data[parent] = data[parent], data[i]
                i = parent
            else:
                break

    def _sift_down(self, i):
        data = self._data
        n = len(data)
        while True:
            left, right = 2 * i + 1, 2 * i + 2
            smallest = i
            if left < n and data[left][0] < data[smallest][0]:
                smallest = left
            if right < n and data[right][0] < data[smallest][0]:
                smallest = right
            if smallest == i:
                break
            data[i], data[smallest] = data[smallest], data[i]
            i = smallest
