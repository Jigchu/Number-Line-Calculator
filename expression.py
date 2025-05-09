from __future__ import annotations

class Expression:
    def __init__(self, command: str):
        self.commands: Token = self.parse(command)

    # TODO: Add functions and inlines and stuff
    def parse(self, command: str):
        commands: Token = Token()

        # Parse additions first
        current = commands
        for segment in command.split(sep="+"):
            current.next = Token(segment)
            current.next.next = Token("+")
            current = current.next.next

        _ = commands.pop()

        # Parse multiplication
        current = commands
        prev = None
        while current is not None:
            if "*" not in current.value:
                prev = current
                current = current.next
                continue
            negative_count = current.value.count("-")
            current.value = current.value.replace("-", "")
            if negative_count % 2 == 0:
                prev = current
                current = current.next
                continue
            if prev is None:
                prev = current
                current = current.next
                continue
            new_token = Token("-", current)
            prev.next = new_token
            prev = current
            current = current.next

        # Parse negatives
        current = commands
        prev = None
        while current is not None:
            if "-" not in current.value:
                prev = current
                current = current.next
                continue
            if len(current.value) == 1:
                prev = current
                current = current.next
                continue

            token = f"\n{current.value}\n"
            token = token.split("-")
            for i in range(len(token)-1, 0, -1):
                token.insert(i, "-")
            token = [term for term in token if term != "\n"]
            token = list(map(lambda s: s.strip(), token))

            buffer = Token(token[0])
            tmp = buffer
            for term in token[1:]:
                new_token = Token(term)
                tmp.next = new_token
                tmp= new_token

            if prev is None:
                break

            prev.next = buffer
            tmp.next = current.next

            prev = tmp
            current = current.next

        return commands

    def run(self, starting_value: int = 0):
        curr_number = starting_value
        direction: int = 1

        current = self.commands.next
        if current is None:
            return curr_number

        while current is not None:
            command = current.value
            match command:
                case "+":
                    pass
                case "-":
                    direction *= -1
                case command if any([c for c in command if c == "*"]):
                    command = command.split("*")
                    curr_number += direction * int(command[0]) * int(command[1])
                case _:
                    curr_number += direction * int(command)
            current = current.next

        return curr_number

# TODO: Make a very fancy iterator for my very fancy linked list

# Fancy class that is just a linked list
class Token:
    def __init__(self, value: str = "", next: Token | None = None):
        self.value: str = value
        self.next: Token | None = next

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

