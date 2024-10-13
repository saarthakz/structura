from typing import List


class Heap:
    def __init__(self, init_vals: List[int] = []):
        self.heap = init_vals
        self.heapify()

    def insert(self, value):
        self.heap.append(value)
        self._heapify_up(len(self.heap) - 1)

    def _heapify_down(self, index):
        left = 2 * index + 1
        right = 2 * index + 2
        largest = index

        if left < len(self.heap) and self.heap[left] > self.heap[largest]:
            largest = left
        if right < len(self.heap) and self.heap[right] > self.heap[largest]:
            largest = right

        if largest != index:
            # Swap with the largest child and heapify down
            self.heap[index], self.heap[largest] = self.heap[largest], self.heap[index]
            self._heapify_down(largest)

    def _heapify_up(self, index):
        if index == 0:
            return

        # Get the parent
        parent = (index - 1) // 2
        if self.heap[index] > self.heap[parent]:
            self.heap[index], self.heap[parent] = self.heap[parent], self.heap[index]
            self._heapify_up(parent)

    def heapify(self):
        for idx in range(len(self.heap) // 2 - 1, -1, -1):
            self._heapify_down(idx)

    def extract_max(self):
        if len(self.heap) == 0:
            return None
        if len(self.heap) == 1:
            return self.heap.pop()
        max = self.heap[0]
        self.heap[0] = self.heap.pop()
        self._heapify_down(0)
        return max
