from __future__ import annotations
from .token import *

FUNCTION_TABLE: dict[str, Function] = {}

# when command is an empty string, expression.commands will be None
class Expression:
    def __init__(self, command: str):
        self.commands: Token | None = None
        if command == "":
            return

        self.commands = self.parse(command)

    def copy(self):
        expression_copy = Expression("")

        if self.commands is None:
            return expression_copy
        commands_copy = self.commands.copy()
        expression_copy.commands = commands_copy

        return expression_copy

    def parse(self, command: str):
        commands = None

        # Parse functions
        segments = command.split(sep="+")
        index = 0
        while index < len(segments):
            segment = segments[index]
            if "(" in segment and ")" not in segment:
                function_segment = [segments[index], segments[index+1]]
                function_segment = "+".join(function_segment)
                segments = segments[:index] + [function_segment] + segments[index+2:]
                index -= 1
            index += 1

        # Remove negatives from functions
        index = 0
        while index < len(segments):
            segment = segments[index]
            if "(" in segment:
                function_segment = segment
                function_segment_ref = function_segment[:]
                function_segment = "".join([c for c in function_segment if c != "-"])
                function_segments: list[str] = []
                if function_segment_ref.startswith("-"): 
                    first_half_segment = function_segment_ref[:len(function_segment_ref)//2]
                    prefixed_negatives = [c for c in first_half_segment if c == "-"]
                    function_segments.extend(prefixed_negatives)
                function_segments.append(function_segment)
                if function_segment_ref.endswith("-"):
                    last_half_segment = function_segment_ref[len(function_segment_ref)//2:]
                    suffixed_negatives = [c for c in last_half_segment if c == "-"]
                    function_segments.extend(suffixed_negatives)
                segments = segments[:index] + function_segments + segments[index+1:]

            index += 1

        commands = Token(segments[0])
        current = commands

        # Parse additions
        for segment in segments[1:]:
            current.next = Token("+")
            current.next.next = Token(segment)
            current = current.next.next


        # Parse multiplication
        for prev, current in commands:
            if "*" not in current.value:
                continue
            if "(" in current.value:
                continue
            negative_count = current.value.count("-")
            current.value = current.value.replace("-", "")
            if negative_count % 2 == 0:
                continue
            if prev is None:
                continue
            new_token = Token("-", next=current)
            prev.next = new_token

        # Parse negatives
        command_iterator = TokenIterator(commands)
        for prev, current in command_iterator:
            if "-" not in current.value or current.type == "Function":
                continue
            if len(current.value) == 1:
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

            tmp_len = tmp.len()

            if prev is None:
                break
            prev.next = buffer
            tmp.next = current.next

            command_iterator.step(tmp_len)

        return commands

    def run(self, starting_value: int = 0) -> int:
        if self.commands is None:
            return starting_value

        curr_number = starting_value
        direction: int = 1
        for _, current in self.commands:
            command = current.value
            added_number = 0
            match command:
                case "+":
                    pass
                case "-":
                    direction *= -1
                case command if current.type == "Function": 
                    name, command = command.split(sep="(")
                    func = FUNCTION_TABLE[name]
                    arg_expression = command.split(sep=")")[0]
                    arg_expression = Expression(arg_expression)
                    func_result= func.run(arg_expression.run())
                    added_number = func_result
                case command if any([c for c in command if c == "*"]):
                    command = command.split(sep="*")
                    expression1 = Expression(command[0])
                    expression2 = Expression(command[1])
                    added_number = expression1.run() * expression2.run()
                case _:
                    added_number = int(command)
            curr_number += direction * int(added_number)

        return curr_number

    @classmethod
    def isexpression(cls, expression: str):
        if expression[0] in ["+", "*"]:
            return False

        return True

class Function:
    def __init__(self, initialisation: str):
        self.name: str = ""
        self.arg_name: str = ""
        self.expression: Expression
        self.base_cases: dict[int, Expression] = {}

        name, arg_name, expression = self.parse(initialisation)
        try:
            arg_name = int(arg_name)
        except ValueError:
            self.name = name
            self.arg_name = arg_name
            self.expression = Expression(expression)
            FUNCTION_TABLE[self.name] = self
            return

        function = FUNCTION_TABLE[name]
        function.base_cases[int(arg_name)] = Expression(expression)

    def parse(self, initialisation: str):
        name, expression = initialisation.split(sep="=")
        expression = "".join(expression).replace(" ", "")

        name, arg_name = name.split(sep="(")
        arg_name = "".join(arg_name).replace(")", "")

        return name, arg_name, expression

    def run(self, arg_value: int) -> int:
        if arg_value in self.base_cases:
            return self.base_cases[arg_value].run()

        command_to_run = self.expression.copy()

        if command_to_run.commands is None:
            return 0

        for _, current in command_to_run.commands:
            current.value = current.value.replace(self.arg_name, str(arg_value))

        return command_to_run.run()


