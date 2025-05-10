import sys

from expression import *

# TODO: Create syntax checking and flags and others
def main():
    starting_value = 0

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
        print(expression.run(starting_value))

    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        sys.exit(0)
