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

        # Parse additions first
        segments = command.split(sep="+")
        tmp_segments = segments.copy()
        for index, segment in enumerate(tmp_segments):
            if "(" in segment and ")" not in segment:
                function_segnment = [tmp_segments[index], tmp_segments[index+1]]
                function_segnment = "+".join(function_segnment)
                segments = segments[:index] + [function_segnment] + segments[index+2:]

        commands = Token(segments[0])
        current = commands

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


class Function:
    def __init__(self, initialisation: str):
        self.name: str = ""
        self.arg_name: str = ""
        self.expression: Expression
        self.base_cases: dict[int, Expression] = {}

        name, arg_name, expression = self.parse(initialisation)
        if arg_name.isnumeric():
            function = FUNCTION_TABLE[name]
            function.base_cases[int(arg_name)] = Expression(expression)
            return

        self.name = name
        self.arg_name = arg_name
        self.expression = Expression(expression)
        FUNCTION_TABLE[self.name] = self

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


