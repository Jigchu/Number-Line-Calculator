import sys

from expression import *

def main():
    starting_value = 0
    CONTINUOUS = "--continuous" in sys.argv or "-c" in sys.argv

    while True:
        command = input("> ").strip()
        if command == "quit":
            break
        if command.startswith("set"):
            starting_value = int(command.split()[1])
            continue

        command = command.replace(" ", "")

        if "=" in command:
            _ = Function(command)
            continue

        expression = Expression(command)
        expression_result = expression.run(starting_value)

        if CONTINUOUS:
            starting_value = expression_result

        print(expression_result)

    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        sys.exit(0)
