from __future__ import annotations
from typing import override

# Fancy class that is just a linked list
class Token:
    def __init__(self, value: str = "", next: Token | None = None):
        self.value: str = value
        self.next: Token | None = next

    @override
    def __str__(self):
        return " -> ".join([current.value for _, current in self])

    def __iter__(self):
        return TokenIterator(self)

    # Removes the last element of the linked list and returns its value or None
    def pop(self):
        last = self
        new_last = None

        for prev, current in self:
            last = current
            new_last = prev

        if new_last is None:
            return None
        new_last.next = None

        return last.value

    def len(self):
        return sum([1 for _ in self])

class TokenIterator:
    def __init__(self, token: Token):
        self.node: Token | None = token
        self.prev: Token | None = None

    def __iter__(self):
        return self

    def __next__(self):
        if self.node is None:
            raise StopIteration

        current = self.node
        prev = self.prev
        self.prev = self.node
        self.node = self.node.next

        return prev, current

    def step(self, steps: int):
        for _ in range(steps):
            if self.node is None or self.node.next is None:
                return
            self.prev = self.node
            self.node = self.node.next

