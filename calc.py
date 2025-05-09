import sys

from Calculator import Calculator

# TODO: Create syntax checking and flags and others
def main():
    starting_value = 0

    while True:
        command = input("> ").strip()
        if command == "quit":
            break
        if command.startswith("set"):
            starting_value = int(command.split()[1])

        command = command.replace(" ", "")

        calculator = Calculator(command)
        print(calculator.run(starting_value))

    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        sys.exit(0)
