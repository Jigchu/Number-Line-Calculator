from __future__ import annotations
from typing import Literal, override

# Fancy class that is just a linked list
class Token:
    def __init__(self, value: str = "", token_type: Literal["Term", "Operator", "Function"] = "Term", next: Token | None = None, copy: bool = False):
        self.value: str = value
        self.type: Literal["Term", "Operator", "Function"] = token_type
        self.next: Token | None = next

        if copy:
            return

        if "*" in self.value:
            self.type = "Term"
        elif "(" in self.value:
            self.type = "Function"
        elif any([c for c in self.value if c in ["+", "-"]]):
            self.type = "Operator"

    @override
    def __str__(self):
        return " -> ".join([current.value for _, current in self])

    def __iter__(self):
        return TokenIterator(self)

    def len(self):
        return sum([1 for _ in self])

    def copy(self):
        head = Token(self.value, self.type, copy=True)

        if self.next is None:
            return head

        copy_current = head
        for _, current in self.next:
            token_copy = Token(current.value, self.type, copy=True)
            copy_current.next = token_copy
            copy_current = token_copy

        return head

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

