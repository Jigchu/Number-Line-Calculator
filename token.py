from __future__ import annotations


# Fancy class that is just a linked list
class Token:
    def __init__(self, value: str = "", next: Token | None = None):
        self.value: str = value
        self.next: Token | None = next

    def __iter__(self):
        return TokenIterator(self)

    # Removes the last element of the linked list and returns its value or None
    def pop(self):
        if self.next is None:
            return None

        current = self
        while current.next is not None:
            if current.next.next is None:
                break
            current = current.next

        last = current.next
        if last is None:
            return None

        current.next = None

        return last.value

class TokenIterator:
    def __init__(self, token: Token):
        self.node: Token = token

    def __next__(self):
        if self.node is None:
            raise StopIteration

        current = self.node
        self.node = self.node.next

        return current
